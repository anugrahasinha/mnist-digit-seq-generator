'''
Example code for using CogentDigitGenerator Python API
'''

# Assuming python path has been updated to include the cogentDigitGen #

# Main Class #
from cogentDigitGen.lib import CogentDigitGenerateSequence

# Standard ReaderClass Reader Class #
from cogentDigitGen.lib import CogentDigitGenerateReadImageData as userClass

class myClass(object):
    def __init__(self):
        pass
    
    def getImage(self,**kwargs):
        obj = CogentDigitGenerateSequence(userClass,**kwargs)
        obj.execute()
        return(obj.outputImageArray,obj.imageMetaInfo)


myObj = myClass()
imageArray,metaInfo = myObj.getImage(digits=[1,3,6,2,6,8],spacingRange=(0,100),imageWidth=500,spacingMode="EQUALIZED_MAX")
print(metaInfo)

''' APPENDIX - A '''
# Custom Image Reader class as per your choice #

# Image Reader Class information :
# You can write your own imageReader, with following specifications 
# Exmaple:
# class myReader(object):
#     def __init__(self,imageFile,labelFile):
#         self.imageFile = imageFile
#         self.labelFile = labelFile
#     
#     def parseImageData(self):   <- This should return a dict which looks something like this 
#                                    { "label1" : [imageArray1_1.numpyArray, imageArray1_2, imageArray1_2],
#                                      "label2" : [imageArray2_1.numpyArray, imageArray2_2]
#                                    }
#                                    imageArray.numpyArray = 2D array, each element as a pixel 
#     ...                     
#----########---
# After having a class like above you can execute like below
# obj = CogentDigitGenerateSequence(myReader)
# obj.execute()
# imageData = obj.outputImageArray
# imageMetaData = obj.imageMetaInfo


''' APPENDIX - B '''
# Options for CogentDigitGenerateSequence, which can set the execution behavior #
# Valid variable names :
#
# imagePath     = <ImageCorpus>
# labelPath     = <labelCorpus>
# digits        = <list of output digits ~ Eg -> [1,2,3,4,5,6,7]
# spacingRange  = <tuple of min,max spacing range> ~ Eq -> (0,100)
# imageWidth    = <final output image width> ~ Eg -> 100
'''spacing_mode = EQUALIZED_MAX or EQUALIZED_MIN or PROGRESSIVE # '''
# spacingMode   = EQUALIZED_MAX
