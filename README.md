# Cogent Digit Sequence Generator
### Background
Python API/ CLI / REST Server for generating random numbered sequences (as per digits provided by user) and MNIST data base for digit images.

The digits are stacked horizontally and the spacing between them follow a uniform distribution over a range determined by two user specified numbers. The numerical values of the digits themselves are provided by the user and each digit in the generated sequence is then chosen randomly from one of its representations in the MNIST dataset. The width of the output image in pixels is specified by the user, while the height should be 28 pixels (i.e. identical to that of the MNIST digits).  The code should contain both an API and a script.


### Working
#### CLI
CLI usage is fairly simple. The help is mentioned below
```
usage: cogentDigitSequenceCLI.py [-h] [-d DIGITS] [-sr SPACINGRANGE]
                                 [-w IMAGEWIDTH] [-i IMAGEPATH] [-l LABELPATH]
                                 [-sm {EQUALIZED_MAX,EQUALIZED_MIN,PROGRESSIVE}]
                                 outputPath

positional arguments:
  outputPath            Processed image output location ~ <full file path>

optional arguments:
  -h, --help            show this help message and exit
  -d DIGITS, --digits DIGITS
                        Digits to be parsed. ~ Eg. [0,1,2,3,4]
  -sr SPACINGRANGE, --spacingRange SPACINGRANGE
                        Spacing Range ~ Eg. (0,100)
  -w IMAGEWIDTH, --imageWidth IMAGEWIDTH
                        Image Width ~ Eg. 500
  -i IMAGEPATH, --imagePath IMAGEPATH
                        Custom Image path ~ <full file path>
  -l LABELPATH, --labelPath LABELPATH
                        Custom Label path ~ <full file path>
  -sm {EQUALIZED_MAX,EQUALIZED_MIN,PROGRESSIVE}, --spacingMode {EQUALIZED_MAX,EQUALIZED_MIN,PROGRESSIVE}
                        Spacing Mode
```
If any of the options are not mentioned then they will be picked up from the default config file.


#### Python API
Download the code from the GitLab repository. Set the PYTHONPATH to point to downloaded directory path.
An example for PYTHONAPI is provided in examples

*Simple usage example*
```python
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
```


*Class based example, with custom reader class*
```python
#Main Class#
from cogentDigitGen.lib import CogentDigitGenerateSequence

#Standard ReaderClass Reader Class #
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
```

##### Constructor information for CogentDigitGenerateSequence
Following options are valid
```
digits       -> Like a list  -> Eq : [1,3,6,2,6,8]
spacingRange -> Like a tuple -> Eq : (0,100)
imageWidth   -> Like a int   -> Eg : 1000
spacingMode  -> [EQUALIZED_MAX | EQUALIZED_MIN | PROGRESSIVE]

userClass    -> You can provide your own user class, which reads a file which you would like to have
                However, CogentDigitGenerateSequence will call constructor of userClass as
                userClass(imageFile, labelFile) <- imageFile/labelFile are present in config file
                Thereafter, CogentDigitGenerateSequence will call userClass.parserImageData()
                
                So for user defined reader class, constructor should take 2 arguments, namely imageFile and labelFile
                (Just like MNIST data files)
                Also it should expose a def parseImageData() function, which will be called from outside world.
                
                The output of parseImageData looks something like this
                { "label1" : [imageArray1_1,imageArray1_2,...],
                  "label2" : [imageArray2_1,imageArray2_2,...]}
```
Every option has a predefined default present in etc/config.ini

#### REST Interface
Use the cogentDigitSequenceRESTServer.py file to deploy this as a REST server.
The default port is 8080
Usage is as follows:
```
usage = {"INFO" : "Help on usage of request string",
         "BASE_URL" : "<IP>:8080/cogentDigitGen?",
         "VALID QUERY STRINGS" : {
             "digits" : "Eg. [0,1,2,3,4] -> DEFAULT = [0,1,2,3,4,5,6,7,8,9] -> (** REQUIRED **)",
             "imageWidth" : "Eg. 1000 -> DEFAULT = 1000 -> (** OPTIONAL **)",
             "spacingRange" : "Eg. (0,100) -> DEFAULT = (0,100) -> (** OPTIONAL **)",
             "spacingMode" : "Eq. [EQUALIZED_MAX | EQUALIZED_MIN | PROGRESSIVE ] -> DEFAULT = EQUALIZED_MAX -> (** OPTIONAL **)"},
         }
```
Output of REST interface is fowarded to a Amazon S3 Bucket. The configurations can be made through config file.
As a default they are being forwarded to 
https://s3.amazonaws.com/cogentoutputpublic/

##### Requirements
Please check requirements from requirements.txt file.