'''
Example code for using CogentDigitGenerator Python API
'''

# Assuming python path has been updated to include the cogentDigitGen #

# Main Class #
from cogentDigitGen.lib import CogentDigitGenerateSequence

# Standard ReaderClass Reader Class #
from cogentDigitGen.lib import CogentDigitGenerateReadImageData as userClass


def generate_numbers_sequence(digits, spacing_range, image_width):
    obj = CogentDigitGenerateSequence(userClass,digits=digits,spacingRange=spacing_range,imageWidth=image_width)
    obj.execute()
    return(obj.outputImageArray)


imageArray = generate_numbers_sequence([1,3,6,2,6,8],(0,100),500)
print(imageArray.shape)
