import logging
import struct
import numpy as np
from array import array

from .cogentLogging import CogentLogging

logger = logging.getLogger("CogentDigitBase.ReadImageData")

class CogentDigitGenerateReadImageData(object):
    def __init__(self,imageFile,imageLabelFile):
        try:
            self.imageFile = imageFile
            self.imageLabelFile = imageLabelFile
        except Exception as e:
            logger.error("Unable to create object for ReadImageData class, exception : %s" %(str(e)))
            raise(e)
    
    def parseImageData(self):
        try:
            return(self.__parseImageData())
        except Exception as e:
            logger.error("Unable to read image data, imageFile = %s & imageLabelFile = %s & exception : %s" %(str(self.imageFile),str(self.imageLabelFile),str(e)))
            raise(e)
            
    def __parseImageData(self):
        try:
            with open(self.imageFile,"rb") as f:
                magicNum, size, rows, cols = struct.unpack(">IIII", f.read(16))
                logger.info("imageFile -> magicNum = %d, size = %d, rows = %d, cols = %d" %(magicNum,size,rows,cols))
                if magicNum != 2051:
                    error = "While reading image data, magic number not as expceted. Expected value = 2051, value received = %d" %(magicNum)
                    logger.error(error)
                    raise(Exception(error))
                image = list(map(lambda px : (255 - px) / 255.0, array("B", f.read())))
                parsed_images = np.asarray(image, dtype=np.float32).reshape(size,rows,cols)
            logger.info("Completed parsing imageFile, number of images read = %d" %(parsed_images.shape[0]))
                
            with open(self.imageLabelFile,"rb") as f:
                magicNum, size = struct.unpack(">II", f.read(8))
                logger.info("imageLabelFile -> magicNum = %d, size = %d" %(magicNum,size))
                if magicNum != 2049:
                    error = "While reading image label data, magic number not as expected. Excepted value = 2049, value received = %d" %(magicNum)
                    logger.error(error)
                    raise(Exception(error))
                parsed_labels = np.array(array("B",f.read())).reshape(size,1)
            logger.info("Completed parsing imageLabelFile, number of labels parsed = %d, unique lables = %s" %(parsed_labels.shape[0],str(np.unique(parsed_labels))))
            
            # Build the final dict #
            # We build a dict which is not restricted to just 0 ~ 9 but any labels which might be present #
            result_dict = dict()
            for label in np.unique(parsed_labels):
                result_dict[str(label)] = parsed_images[np.where(label == parsed_labels)[0],:,:]
            logger.info("For unique image labels as %s, the number of images found = %s totalling = %d images in the dict" %(str(np.unique(parsed_labels)),
                                                                                                                                 str([result_dict[str(x)].shape[0] for x in np.unique(parsed_labels)]),
                                                                                                                                 sum([result_dict[str(x)].shape[0] for x in np.unique(parsed_labels)])))
            return(result_dict)
        except Exception as e:
            raise(e)