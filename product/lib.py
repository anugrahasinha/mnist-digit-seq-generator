import numpy as np
import struct

'''
Base class builts some class variables, in a singleton manner, in order to
    optimize execution time, so that 
    1. File open/close operations could be limited at every call
    2. reference of the MNIST DB Data is available in memory
        as a dictionary reference. This is light weight dictionary,
        hence low memory consumption.
'''
class Base:

    # Class variables #
    __mnist_data_file_obj__ = None
    __mnist_label_dict__ = None
    
    '''
        This function creates a dict reference, for each number
        as to which index does it appear in image database
        it looks like this
        { 0 : [3,10,13,25,28 ...],
          1 : [2,5,14,29,31,37...],
          ...
        }
        
        This enables to perform a f.seek operation easily on
        mnist image DB, get the image as per index provided

        Parameters
        ----------------------
        mnist_data_file_name : str
            

        Return
        ----------------------
        label_dict : dict
            dictionary refernce as per information mentioned above.
    '''

    @classmethod
    def setup(self,mnist_data_file_name, mnist_label_file_name):
        if Base.__mnist_data_file_obj__ is None or Base.__mnist_label_dict__ is None:
            # read the label file and get the 
            with open(mnist_label_file_name,"rb") as f_obj:
                Base.__mnist_label_dict__ = {x : list() for x in range(10)}
                _ = struct.unpack('>i',f_obj.read(4))[0] # magic number
                n_labels = struct.unpack('>i',f_obj.read(4))[0]

                for idx in range(n_labels):
                    l = struct.unpack('B',f_obj.read(1))[0]
                    Base.__mnist_label_dict__[l].append(idx)
            
            # Open data file and get the file obj created a class variable for reference
            Base.__mnist_data_file_obj__ = open(mnist_data_file_name,"rb")

'''
This is the library class exposed to seq_generator.py
1. A constructor for this class will be built up at every call of API (create_digit_sequence)
    However, due to inheritence and singleton nature of Base class, reference dict and image
    data file object will be created only once.
2. The above ensures that multiple calls to API (create_digit_sequence), does not result in 
    multiple reference dictionary creation and also avoid multiple FD (file descriptors)
    being opened for same image data file.

'''

class mnist_digit_seq_gen(Base):

    def __init__(self,mnist_data_file_name, mnist_label_file_name):
        # Instantiate the Base class #
        super().setup(mnist_data_file_name, mnist_label_file_name)

    def get_image(self,num, n_rows = 28, n_cols = 28, initial_offset = 16):
        '''
        Given a specific number, it will read a random image for that number
        in the MNIST image DB

        Parameters
        ----------------------
        num : int
            This should be number between [0,9]
        n_rows : int
            This is the number of rows in the array of the image that is read from DB.
            Default : 28 (Same as MNIST)
        n_cols : int
            This is the number of cols in the array of the image that is read from DB.
            Default : 28 (Same as MNIST)
        initial_offset : int
            This is the initial file read offset for image DB file.
            Default : 16 (Same as MNIST)

        Return
        ----------------------
        image : numpy.array
            image read from MNIST DB. 
            Pixel values are 0 to 255. 0 means background (white), 255 means foreground (black).
        '''
        img = []
        label_dict = self.__mnist_label_dict__
        idx = np.random.choice(label_dict[num])
        self.__mnist_data_file_obj__.seek((idx * n_rows * n_cols) + initial_offset)
        img = [ struct.unpack('B',self.__mnist_data_file_obj__.read(1)) for x in range(n_rows*n_cols)]
        return np.array(img).reshape(n_rows,n_cols)

    def get_spacings(self,n_digits, image_width, min_spacing, max_spacing, per_image_width=28):
        '''
        Given the number of digits to be 'drawn' & image_width, and spacing
        parameters, this sub-routine checks if the provided values are favorable
        and subsequently, provides the spacing to be used between digits.

        Parameters
        ----------------------
        n_digits : int
            The number of digits that are needed to be drawn
        image_width : int
            Final image width in pixels
        min_spacing : int
            min spacing required in pixels
        max_spacing : int
            max spacing required in pixels
        per_image_width : int
            Image width of the number which will be read. Assumes that all
            numbers will be of the same dimensions
            Default : 28 (Same as MNIST)

        Return
        ----------------------
        Success : Appropriate spacing to be used
        Failure : Raises ValueError with appropriate message
        '''
        min_size = n_digits * per_image_width
        blank_space = image_width - min_size
        
        # This is for edge to edge plotting, that means no space on left and right #
        #cal_spacing = blank_space // (n_digits - 1)
        
        # This is for evenly spaced plotting, that means spacing at beginning and end also #
        cal_spacing = blank_space // (n_digits + 1)
        if cal_spacing < min_spacing or cal_spacing > max_spacing:
            raise ValueError("image_width : %d(px), min_spacing : %d(px) & max_spacing : %d(px) is not optimum for n_digits : %d" \
                            %(image_width,min_spacing,max_spacing,n_digits))
        
        # For equal spacing we can use
        #return [ cal_spacing for x in range(n_digits) ]

        # For random spacing between digits we can use
        # Option 1 : We do a random int sampled from range(cal_spacing)
        #            This would generally bring values closer to cal_spacing / 2 
        #            and final output will generally have right side of the image empty.
        #            This is not optimum for an AI/ML model to generalize
        # Option 2 : We sample from 75th to 100th percentile, this would ensure
        #            higher numbers, and hence almost complete space would be occupied
        # Option 3 : We do a progressive spacing, which will be complex to implement,
        #            but may be favored. Currently, keeping that as "SCOPE OF IMPROVEMENT"

        # Going with Option 2
        lower, upper = int(np.quantile(range(cal_spacing),0.75)), int(np.quantile(range(cal_spacing),1.0))
        spacings = [ np.random.choice(range(lower,upper)) for x in range(n_digits + 1) ]
        #print("spacings : ",spacings)
        return spacings