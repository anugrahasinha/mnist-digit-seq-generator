import argparse
import logging
import traceback
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime
import ast
import re
import boto3
import tempfile

# Cogent Specific Imports #
from .cogentLogging import CogentLogging
from .cogentConfigParser import CogentConfigParser

logger = logging.getLogger("CogentDigitBase.Utils")

class CogentUtils(object):
    def __init__(self):
        pass
    
    def parseCLIArguments(self):
        try:
            options = { "digits" : None,
                        "spacingRange" : None,
                        "imageWidth" : None,
                        "imagePath" : None,
                        "labelPath" : None,
                        "outputPath" : None,
                        "spacingMode" : None,
                        "whitePixel" :None }
            parser = argparse.ArgumentParser()
            parser.add_argument("-d","--digits",help="Digits to be parsed. ~ Eg. [0,1,2,3,4]")
            parser.add_argument("-sr","--spacingRange",help="Spacing Range ~ Eg. (0,100)")
            parser.add_argument("-w","--imageWidth",help="Image Width ~ Eg. 500")
            parser.add_argument("-i","--imagePath",help="Custom Image path ~ <full file path>")
            parser.add_argument("-l","--labelPath",help="Custom Label path ~ <full file path>")
            parser.add_argument("-sm","--spacingMode",help="Spacing Mode",choices = ["EQUALIZED_MAX","EQUALIZED_MIN","PROGRESSIVE"])
            parser.add_argument("outputPath",help="Processed image output location ~ <full file path>")            
            args = parser.parse_args()
            
            if bool(args.imagePath) ^ bool(args.labelPath):
                logger.error("ERROR : imagePath and labelPath both should be provided together")
                parser.print_usage(sys.stdout)
                raise(Exception("ERROR : imagePath and labelPath both should be provided together"))
            if args.spacingRange and not re.search("^(.+)$",args.spacingRange):
                logger.error("ERROR : spacingRange %s is not provided as a tuple" %(args.spacingRange))
                parser.print_usage(sys.stdout)
                raise(Exception("ERROR : spacingRange %s is not provided as a tuple" %(args.spacingRange)))
            
            if args.digits and not re.search("^\[.+\]$",args.digits):
                logger.error("ERROR : digits %s is not provided as a list" %(args.digits))
                parser.print_usage(sys.stdout)
                raise(Exception("ERROR : digits %s is not provided as a list" %(args.digits)))
            
            if not self.validatePath(args.outputPath,"dir"):
                logger.error("ERROR : outputPath %s does not exist" %(args.outputPath))
                parser.print_usage(sys.stdout)
                raise(Exception("ERROR : outputPath %s does not exist" %(args.outputPath)))
            
            
            logger.debug("User inputs = %s" %(str(args)))
            return dict(args._get_kwargs())
        except Exception as e:
            logger.error("Error while parsing CLI Arguments, exception : %s" %(str(e)))
            logger.error("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))
            raise(e)
    
    def validatePath(self,path,checkType):
        try:
            if checkType == "dir":
                return(os.path.exists(os.path.dirname(os.path.realpath(path))))
            elif checkType == "file":
                return(os.path.exists(os.path.realpath(path)))
            else:
                return False
        except Exception as e:
            logger.error("Exception in checking validity of path = %s, checkType = %s" %(path,checkType))
            raise(e)
       
    def validateUserArguments(self,**kwargs):
        try:
            configObj = CogentConfigParser()
            logger.debug("User provided inputs being validated : %s" %(str(kwargs)))
            parsedOptions = dict()
            # digits #
            parsedOptions["digits"] = ast.literal_eval(str(kwargs.get("digits"))) if kwargs.get("digits") else ast.literal_eval(configObj.parser["CogentDigitGenerator"]["digits"])
            if not isinstance(parsedOptions["digits"],list):
                logger.error("Digits is not a list. Given Digits = %s" %(str(parsedOptions["digits"])))
                raise(Exception("ERROR: Digits is not  given as a list"))
            
            # spacing_range #
            parsedOptions["spacing_range"] = ast.literal_eval(str(kwargs.get("spacingRange"))) if kwargs.get("spacingRange") else ast.literal_eval(configObj.parser["CogentDigitGenerator"]["spacingRange"])
            if not isinstance(parsedOptions["spacing_range"],tuple):
                logger.error("spacing_range is not tuple. Given : %s" %(str(parsedOptions["spacing_range"])))
                raise(Exception("ERROR : spacingRange is not a tuple"))
            
            # image_width #
            parsedOptions["image_width"] = ast.literal_eval(str(kwargs.get("imageWidth"))) if kwargs.get("imageWidth") else ast.literal_eval(configObj.parser["CogentDigitGenerator"]["imageWidth"])
            if not isinstance(parsedOptions["image_width"],int):
                logger.error("image_width is not a integer. Given : %s" %(str(parsedOptions["image_width"])))
                raise(Exception("ERROR : imageWidth is not a integer"))
            
            # spacing_mode #         
            parsedOptions["spacing_mode"] = str(kwargs.get("spacingMode")) if kwargs.get("spacingMode") else configObj.parser["CogentDigitGenerator"]["spacingMode"]
            if not re.search("(^(EQUALIZED){1}_{1}(MAX|MIN)$|^(PROGRESSIVE)$)",parsedOptions["spacing_mode"]):
                logger.error("spacing_mode is not properly given. Given : %s" %(str(parsedOptions["spacing_mode"])))
                raise(Exception("ERROR : spacingMode is not given properly"))
            
            # imageFile #
            parsedOptions["image_file"] = str(kwargs.get("imagePath")) if kwargs.get("imagePath") else configObj.parser["CogentDigitGenerator"]["imagePath"]
            if not self.validatePath(parsedOptions["image_file"],checkType="file"):
                logger.error("imageFile not found. Given : %s" %(parsedOptions["image_file"]))
                raise(Exception("imageFile not found"))
            
            # labelFile #
            parsedOptions["image_label_file"] = str(kwargs.get("labelPath")) if kwargs.get("labelPath") else configObj.parser["CogentDigitGenerator"]["labelPath"]
            if not self.validatePath(parsedOptions["image_label_file"],checkType="file"):
                logger.error("labelPath not found. Given : %s" %(parsedOptions["image_label_file"]))
                raise(Exception("labelPath not found"))
            
            # __whitePixel
            parsedOptions["whitePx"] = ast.literal_eval(configObj.parser["CogentDigitGenerator"]["whitePixel"])
            
            logger.debug("Final options set for operations = %s" %(str(parsedOptions)))
            return parsedOptions
        except Exception as e:
            logger.error("Validation of user arguments failed. Exception : %s" %(str(e)))
            raise(e)
    
    def dumpImage(self,path,imageArray,imageMetaInfo):
        try:
            filename = os.path.realpath(path + "/" + "CogentDigitSequence_" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-1] + "_" + imageMetaInfo["fullImageSize"].strip("(").strip(")").replace(", ","_") + ".jpg")
            logger.info("Writing image to output file = %s" %(filename))
            plt.imsave(fname=filename,arr=imageArray,cmap="gray")
            return filename
        except Exception as e:
            logger.error("Unable to save image, size = %s, filename = %s, exception = %s" %(imageMetaInfo["fullImageSize"],filename,str(e)))
            # do not raise error, send back bool False #
            return False
        
    def dumpImageAWS(self,imageArray,imageMetaInfo):
        try:
            tempDumpedImage = self.dumpImage(os.path.realpath(tempfile.gettempdir()),imageArray,imageMetaInfo)
            logger.debug("Temporary output image created at : %s" %(str(tempDumpedImage)))
            configObj = CogentConfigParser()
            k1 = configObj.parser["CogentAWSInfo"]["K1"]
            k2 = configObj.parser["CogentAWSInfo"]["K2"]
            bucket = configObj.parser["CogentAWSInfo"]["bucket"]
            area = configObj.parser["CogentAWSInfo"]["area"]
            
            connection = boto3.client(service_name="s3",region_name=area,aws_access_key_id=k1,aws_secret_access_key=k2)
            s3_filename = tempDumpedImage.split(os.path.dirname(tempDumpedImage))[1].split("\\")[1]
            connection.upload_file(tempDumpedImage,bucket,s3_filename)
            response = connection.put_object_acl(Bucket=bucket,Key=s3_filename,ACL="public-read")
            logger.info("Uploaded file to AWS at bucket : %s, with filename = %s, Public acccess grand HTTP response : %s" %(str(bucket),str(s3_filename),str(response["ResponseMetadata"]["HTTPStatusCode"])))
            
            os.unlink(tempDumpedImage)
            logger.info("Temporary file : %s, has been deleted" %(str(tempDumpedImage)))
            
            return("https://s3.amazonaws.com/"+bucket+"/"+s3_filename)
        except Exception as e:
            logger.error("Error in uploading file to aws, error : %s" %(str(e)))
            raise(e)