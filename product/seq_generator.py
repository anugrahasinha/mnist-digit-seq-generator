import numpy as np
from .lib import mnist_digit_seq_gen

'''
----------------------
Note
----------------------
1. Currently, the MNIST data is being provided along with code.
    Therefore, the data path filenames are hard coded.
    However, from final product perspective, we can think of 
    building a setup.py file, which on pip installation
    would download the data and save it to users $HOME.
'''

def create_digit_sequence(number, image_width, min_spacing, max_spacing, 
                          data_file="product/data/t10k-images-idx3-ubyte",
                          label_file="product/data/t10k-labels-idx1-ubyte"):
    '''
    A function that creates an image representing the given number,
    with random spacing between the digits.

    Each digit is randomly sampled from the MNIST dataset

    Returns an NumPy array representing the image.

    Parameters
    ----------------------
    number : str
        A string representing the number, eg "14543"
    image_width : int
        The image width (in pixel)
    min_spacing : int
        The minimum spacing between digits (in pixel)
    max_spacing : int
        The maximum spacing between digits (in pixel)
    '''
    try:
        n_rows = 28
        number_list = [int(x) for x in number]
        image = np.zeros((n_rows,image_width))
        lib_obj = mnist_digit_seq_gen(data_file,label_file)
        spacings = lib_obj.get_spacings(len(number_list),image_width,min_spacing,max_spacing)
        s_w_px = 0
        for idx, num in enumerate(number_list): 
            num_image = lib_obj.get_image(num)
            # This is for edge to edge plotting 
            # (when same spacing is being used, not random spacing) #
            #s_w_px = (idx * spacing) + (idx * num_image.shape[1])
            
            # This is for evenly spaced plotting, even at start and beginning 
            # (when same spacing is being used, not random spacing)
            #s_w_px = ((idx+1) * spacings[idx]) + (idx * num_image.shape[1])
            
            # This is when we are using random spacing, specifically to avoid
            # overlapping issue

            if idx == 0:
                s_w_px = spacings[idx]
            else:
                s_w_px += num_image.shape[1] + spacings[idx]
            image[:,s_w_px:s_w_px + num_image.shape[1]] = num_image
        return image
    except Exception as e:
        raise e