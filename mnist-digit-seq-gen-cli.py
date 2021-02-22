import os
import argparse
import matplotlib.pyplot as plt
import traceback
from product.seq_generator import create_digit_sequence

def check_input_number(input_string):
    '''
    Checks whether the input number is a complete integer or not

    Parameters
    -------------------
    input_string : str
        The input number in the form of string provded by user
    
    Return
    -------------------
    Success : returns the same string
    Failure : Raises argparse.ArgumentTypeError
    '''
    try:
        _ = int(input_string)
    except Exception as e:
        print("Error in input number, unknown character '%s'.\n%s" %(input_string,str(e)))
        traceback.print_exc()
        raise argparse.ArgumentTypeError
    return input_string

def check_file_path(input_string):
    '''
    Checks whether the dirname provided for output file exists or not

    Parameters
    -------------------
    input_string : str
        The filepath provided by user

    Return
    -------------------
    Success : returns the same string
    Failure : Raises argparse.ArgumentTypeError
    '''
    dirname = os.path.dirname(input_string)
    if not os.path.exists(dirname):
        print("Path does not exist : %s" %(dirname))
        traceback.print_exc()
        raise argparse.ArgumentTypeError
    return input_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                             description="MNIST Digit Sequence Generator")
    
    parser.add_argument("-n","--number",required=True,
                        type=check_input_number,
                        help="The number which needs to built")
    parser.add_argument("-w","--image-width",required=True,
                        type=int,
                        help="Width of final image")
    parser.add_argument("-misp","--min-spacing",required=True,
                        type=int,
                        help="Minimum spacing required between digits")
    parser.add_argument("-mxsp","--max-spacing",required=True,
                        type=int,
                        help="Maximum spacing required between digits")
    parser.add_argument("-f","--file",required=True,
                        type=check_file_path,
                        help="Full path for output filename")

    try:
        args = parser.parse_args()
        output = create_digit_sequence(args.number,args.image_width,args.min_spacing,args.max_spacing)
        plt.imsave(args.file,1-output,cmap="gray")
    except Exception as e:
        print("[ERROR] : Unable to process request\n%s" %(str(e)))
        traceback.print_exc()
        raise e