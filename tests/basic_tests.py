import os
import sys
from datetime import datetime
import traceback

def printStdOutMessage(message):
    """
    Function responsible for printing out STDOUT message when starting CLI program
    
    Arg: message -> "Message required to be printed"
    Return : <None>
    """
    try:
        base_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + " : cogentDigitSequenceGenerator : Message : "
        print(base_str + message)
    except Exception as e:
        raise(e)

def __setupLocations(customLocation=None):
    """
    Function responsible for setting up location for library in python path
    and setting up current directory locations
    
    Args: <NONE>
    Output: <None>
    """
    try:
        printStdOutMessage("Setting up library locations")
        if customLocation:
            printStdOutMessage("User provided custom location for library setup")
            package_dir = customLocation
        else:
            package_dir = os.path.dirname(os.path.realpath(__file__)) + "/../"
        sys.path.append(package_dir)
        os.chdir(package_dir)
    except Exception as e:
        printStdOutMessage("Unable to setup locations, exception : %s" %(str(e)))
        raise(e)

def readerClassTest():
    from cogentDigitGen.lib import CogentDigitGenerateReadImageData
    imageFile = os.path.realpath("./cogentDigitGen/data/t10k-images.idx3-ubyte")
    labelFile = os.path.realpath("./cogentDigitGen/data/t10k-labels.idx1-ubyte")
    obj = CogentDigitGenerateReadImageData(imageFile,labelFile)
    result = obj.parseImageData()
    if (len(result.keys()) == 10):
        return True
    else:
        return False
    
def imageGeneratorTest():
    from cogentDigitGen.lib import CogentDigitGenerateSequence
    from cogentDigitGen.lib import CogentDigitGenerateReadImageData
    
    imageFile = os.path.realpath("./cogentDigitGen/data/t10k-images.idx3-ubyte")
    labelFile = os.path.realpath("./cogentDigitGen/data/t10k-labels.idx1-ubyte")
    
    obj = CogentDigitGenerateSequence(CogentDigitGenerateReadImageData,
                                      imagePath = imageFile,
                                      labelPath = labelFile,
                                      digits=[1,2,3,4,5],
                                      imageWidth=140,
                                      spacingRange=(0,100),
                                      spacingMode="EQUALIZED_MAX")
    result = obj.execute()
    result = obj.imageMetaInfo
    if result["fullImageSize"] == "(28, 140)" and result["leftMargin"] == "0" and result["rightMargin"] == "0" and result["betweenMargins"] == "[0 0 0 0 0]" and result["numberOfLabels"] == "5":
        return True
    else:
        return False
    
if __name__ == "__main__":
    __setupLocations()
    printStdOutMessage("Starting with basic tests")
    printStdOutMessage("Reader Class Test")
    test1 = readerClassTest()
    printStdOutMessage("Result : Passed = %s" %(str(test1)))
    printStdOutMessage("Sequence Generator Test")
    test2 = imageGeneratorTest()
    printStdOutMessage("Result : Passed = %s" %(str(test2)))
    if test1 and test2:
        sys.exit(0)
    else:
        sys.exit(127)
    
    