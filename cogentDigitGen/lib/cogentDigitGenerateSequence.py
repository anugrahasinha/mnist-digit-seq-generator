# Base python based imports #
import logging
import ast
import traceback
import numpy as np
import json
import re
# Custom program based imports #
from .cogentConfigParser import CogentConfigParser
from .cogentLogging import CogentLogging
from .cogentDigitGenerateReadImageData import CogentDigitGenerateReadImageData
from .cogentUtils import CogentUtils

logger = logging.getLogger("CogentDigitBase.DigitGenSequence")

class CogentDigitGenerateSequence(object):
    def __init__(self,readerClass,**kwargs):
        try:
            self.configObj = CogentConfigParser()
            
            self.parsedOptions = CogentUtils().validateUserArguments(**kwargs)
            self.digits = self.parsedOptions["digits"]
            self.spacing_range = self.parsedOptions["spacing_range"]
            self.image_width = self.parsedOptions["image_width"]
            self.image_file = self.parsedOptions["image_file"]
            self.image_label_file = self.parsedOptions["image_label_file"]
            self.spacing_mode = self.parsedOptions["spacing_mode"]
            self.__whitePx = self.parsedOptions["whitePx"]
            
            self.outputImageArray = None
            self.imageMetaInfo = None               
            
            self.readerObj = readerClass(self.image_file,self.image_label_file)                     
            
            self.__parsedSourceImageData = None
            self.__selectedRawImageArray = None            
        except Exception as e:
            logger.error("Unable to build CogentDigitGenerateSequence Object, exception : %s" %(str(e)))
            logger.exception(e)
            raise(e)
    
    def execute(self):
        try:
            self.__readImageData()
            self.__generateOutputImageArray()
        except Exception as e:
            logger.error("Failed to execute image sequence builder, exception : %s" %(str(e)))
            logger.error("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))
            raise(e)
            
    def __readImageData(self):
        try:
            #readerObj = CogentDigitGenerateReadImageData(self.image_file,self.image_label_file)
            self.__parsedSourceImageData = self.readerObj.parseImageData()
        except Exception as e:
            raise(e)
        
    def __generateOutputImageArray(self):
        try:
            self.__selectedRawImageArray = self.__selectRawImages()
            self.outputImageArray, self.imageMetaInfo = self.__processImages()
            # testing #
            #import matplotlib.pyplot as plt
            #plt.imshow(self.outputImageArray,cmap="gray")
        except Exception as e:
            raise(e)
        
    def __selectRawImages(self):
        try:
            # We should make a list of rawImages so that the order of input given in digits can be maintained #
            rawImageList = list()
            logger.info("User input digit list = %s" %(str(self.digits)))
            for user_digit in self.digits:
                if str(user_digit) in self.__parsedSourceImageData.keys():
                    images_for_digit = self.__parsedSourceImageData[str(user_digit)]
                    # assuming 1 image per digit, if user expects to have multiple images of same digit, then he should have repeated numbers in digit list #
                    chosen_image_idx = np.random.choice(np.arange(0,images_for_digit.shape[0]),1,replace=False)
                    chosen_image = images_for_digit[chosen_image_idx,:,:]
                    chosen_image = chosen_image.reshape(chosen_image.shape[1],chosen_image.shape[2])
                    logger.debug("For user input digit = %s, chosen index from in-memory dict = %d" %(str(user_digit),chosen_image_idx))
                    rawImageList.append(chosen_image)
                else:
                    error = "user provided digit = %s, not present in image data base. Unique image labels are : %s" %(str(user_digit),str(self.__parsedSourceImageData.keys()))
                    logger.error(error)
                    raise(Exception(error))
            return(rawImageList)
        except Exception as e:
            raise(e)
        
    def __processImages(self):
        try:
            # We calculate the minimum space required based on sum of width of selected images. 
            minRequiredWidth = sum([x.shape[1] for x in self.__selectedRawImageArray])
            if minRequiredWidth > self.image_width:
                error = "User input image width = %d is (less than) sum of width of selected images = %d." %(self.image_width,minRequiredWidth)
                logger.error(error)
                raise(Exception(error))
            
            # For equalized spacing #
            if (re.search("^(EQUALIZED){1}_{1}(MAX|MIN)$",self.spacing_mode)):
                # Processing for EQUALIZED MODE #
                rightEndWhiteSpaceLeft = self.image_width - (minRequiredWidth + ((len(self.__selectedRawImageArray) -1) * np.arange(self.spacing_range[0],self.spacing_range[1]+1,1)))
                if not len(np.where(rightEndWhiteSpaceLeft >= 0)[0]) > 0:
                    error = "For spacing_mode = %s,\
                    with min spacing_range = %d and\
                    max spacing range = %d,\
                    image_width = %d and\
                    totalWidthOfAllImages = %d, fitting is not possible.\n\
                    RightEndSpacingLeft = %s" %(self.spacing_mode,
                                                self.spacing_range[0],
                                                self.spacing_range[1],
                                                self.image_width,
                                                minRequiredWidth,
                                                str(rightEndWhiteSpaceLeft))
                    logger.error(error)
                    raise(Exception(error))             
                
                if (self.spacing_mode == "EQUALIZED_MAX"):
                    equalized_min_max_func = min
                else:
                    equalized_min_max_func = max
                
                logger.debug("User selected spacing mode = %s" %(self.spacing_mode))
                
                selectedBetweenSpace = (np.arange(self.spacing_range[0],self.spacing_range[1]+1,1)[np.where(rightEndWhiteSpaceLeft == equalized_min_max_func(rightEndWhiteSpaceLeft[np.where(rightEndWhiteSpaceLeft >= 0)]))])[0]
                leftSpace = int(equalized_min_max_func(rightEndWhiteSpaceLeft[np.where(rightEndWhiteSpaceLeft >= 0)]) / 2)
                rightSpace = equalized_min_max_func(rightEndWhiteSpaceLeft[np.where(rightEndWhiteSpaceLeft >= 0)]) - leftSpace
                
                if ((leftSpace + minRequiredWidth + (selectedBetweenSpace * (len(self.__selectedRawImageArray) - 1)) + rightSpace) != self.image_width):
                    error = "FATAL ERROR : user image width = %d, betweenspace = %d, leftspace = %d, rightspace = %d, SUMMATION DOES NOT MATCH, CHECK LOGS" %(self.image_width,selectedBetweenSpace,leftSpace,rightSpace)
                    logger.error(error)
                    raise(Exception(error))
                
                maxHeightAmongAllImages = max([x.shape[0] for x in self.__selectedRawImageArray])
                
                logger.debug("betweenspace = %d, leftspace = %d, rightspace = %d, maxheight = %d" %(selectedBetweenSpace,leftSpace,rightSpace,maxHeightAmongAllImages))
                
                selectedBetweenSpaceArray = np.repeat(self.__whitePx,(maxHeightAmongAllImages*selectedBetweenSpace)).reshape(maxHeightAmongAllImages,selectedBetweenSpace)
                leftSpaceArray = np.repeat(self.__whitePx,(maxHeightAmongAllImages*leftSpace)).reshape(maxHeightAmongAllImages,leftSpace)
                rightSpaceArray = np.repeat(self.__whitePx,(maxHeightAmongAllImages*rightSpace)).reshape(maxHeightAmongAllImages,rightSpace)
                
                logger.debug("\n\
                selectedBetweenSpace = %d\n\
                leftSpace = %d\n\
                rightSpace = %d\n\
                maxHeightAmongAllImages = %d\n\
                selectedBetweenSpaceArray.shape = %s\n\
                leftSpaceArray.shape = %s\n\
                rightSpaceArray.shape = %s\n\
                rightEndWhiteSpaceLeft.shape = %s\n\
                rightEndWhiteSpaceLeft (array) = %s" %(selectedBetweenSpace,leftSpace,rightSpace,maxHeightAmongAllImages,str(selectedBetweenSpaceArray.shape),
                                                       str(leftSpaceArray.shape),str(rightSpaceArray.shape),str(rightEndWhiteSpaceLeft.shape),str(rightEndWhiteSpaceLeft)))
                
                # modify the height of each selected image to match maxHeightAmongAllImages # <- TO BE DONE
                
                finalImage = self.__selectedRawImageArray[0]
                for image in self.__selectedRawImageArray[1:]:
                    logger.debug("finalImage before white space addition = %s" %(str(finalImage.shape)))
                    finalImage = np.hstack((finalImage,selectedBetweenSpaceArray,image))
                    logger.debug("finalImage after white space addition = %s" %(str(finalImage.shape)))
                
                finalImage = np.hstack((leftSpaceArray,finalImage,rightSpaceArray))
                            
                imageMetaInfo = dict()
                imageMetaInfo["fullImageSize"] = str((maxHeightAmongAllImages,leftSpace + minRequiredWidth + (selectedBetweenSpace * (len(self.__selectedRawImageArray) - 1)) + rightSpace))
                imageMetaInfo["leftMargin"] = str(leftSpace)
                imageMetaInfo["rightMargin"] = str(rightSpace)
                imageMetaInfo["betweenMargins"] = str(np.repeat(selectedBetweenSpace,len(self.__selectedRawImageArray)))
                imageMetaInfo["numberOfLabels"] = str(len(self.__selectedRawImageArray))
                
                logger.debug("finalImage FINALLY = %s" %(str(finalImage.shape)))
                logger.info("FINAL PROCESSED IMAGE METAINFO :\n%s" %(json.dumps(imageMetaInfo,indent=2)))
            else:
                # Processing for PROGRESSIVE MODE #
                selectedBetweenSpace = np.arange(self.spacing_range[0],self.spacing_range[1]+1,1)[0:len(self.__selectedRawImageArray) - 1]
                rightEndWhiteSpaceLeft = self.image_width - (minRequiredWidth + sum(selectedBetweenSpace))
                if (rightEndWhiteSpaceLeft < 0):
                    error = "For spacing_mode = %s, with min spacing_range = %d and max spacing range = %d,image_width = %d and totalWidthOfAllImages = %d,selectedBetweenSpace = %s fitting is not possible.\nRightEndSpacingLeft = %d" %(self.spacing_mode,
                                                                                                                                                                                                                                           self.spacing_range[0],
                                                                                                                                                                                                                                           self.spacing_range[1],
                                                                                                                                                                                                                                           self.image_width,
                                                                                                                                                                                                                                           minRequiredWidth,
                                                                                                                                                                                                                                           str(selectedBetweenSpace),
                                                                                                                                                                                                                                           rightEndWhiteSpaceLeft)
                    logger.error(error)
                    raise(Exception(error))
                
                leftSpace = int(rightEndWhiteSpaceLeft / 2)
                rightSpace = rightEndWhiteSpaceLeft - leftSpace
                
                if ((leftSpace + minRequiredWidth + sum(selectedBetweenSpace) + rightSpace) != self.image_width):
                    error = "FATAL ERROR : user image width = %d, betweenspace = %d, leftspace = %d, rightspace = %d, SUMMATION DOES NOT MATCH, CHECK LOGS" %(self.image_width,selectedBetweenSpace,leftSpace,rightSpace)
                    logger.error(error)
                    raise(Exception(error))
                
                maxHeightAmongAllImages = max([x.shape[0] for x in self.__selectedRawImageArray])
                
                logger.debug("betweenspace = %s, leftspace = %d, rightspace = %d, maxheight = %d" %(str(selectedBetweenSpace),leftSpace,rightSpace,maxHeightAmongAllImages))
                
                leftSpaceArray = np.repeat(self.__whitePx,(maxHeightAmongAllImages*leftSpace)).reshape(maxHeightAmongAllImages,leftSpace)
                rightSpaceArray = np.repeat(self.__whitePx,(maxHeightAmongAllImages*rightSpace)).reshape(maxHeightAmongAllImages,rightSpace)                
                
                finalImage = self.__selectedRawImageArray[0]
                for itr in np.arange(1,len(self.__selectedRawImageArray),1):
                    logger.debug("finalImage before white space addition = %s" %(str(finalImage.shape)))
                    selectedBetweenSpaceArray = np.repeat(self.__whitePx,maxHeightAmongAllImages*selectedBetweenSpace[itr-1]).reshape(maxHeightAmongAllImages,selectedBetweenSpace[itr-1])
                    image = self.__selectedRawImageArray[itr]
                    finalImage = np.hstack((finalImage,selectedBetweenSpaceArray,image))
                    logger.debug("finalImage after white space addition = %s" %(str(finalImage.shape)))
                
                finalImage = np.hstack((leftSpaceArray,finalImage,rightSpaceArray))
                
                imageMetaInfo = dict()
                imageMetaInfo["fullImageSize"] = str((maxHeightAmongAllImages,leftSpace + minRequiredWidth + sum(selectedBetweenSpace) + rightSpace))
                imageMetaInfo["leftMargin"] = str(leftSpace)
                imageMetaInfo["rightMargin"] = str(rightSpace)
                imageMetaInfo["betweenMargins"] = str(selectedBetweenSpace)
                imageMetaInfo["numberOfLabels"] = str(len(self.__selectedRawImageArray))
            
                logger.debug("finalImage FINALLY = %s" %(str(finalImage.shape)))
                logger.info("FINAL PROCESSED IMAGE METAINFO :\n%s" %(json.dumps(imageMetaInfo,indent=2)))
                
            return finalImage,imageMetaInfo
            
        except Exception as e:
            raise(e)