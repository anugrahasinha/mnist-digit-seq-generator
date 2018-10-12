from .cogentConfigParser import CogentConfigParser
import logging
import os
import tempfile
from datetime import datetime

class CogentLogging:
    def __init__(self):
        configParserObj = CogentConfigParser().parser
        self.logger = logging.getLogger("CogentDigitBase")
        
        # Just keeping it as default #
        self.logLevel = logging.DEBUG 
        
        # Set Log Level #
        if configParserObj.get('CogentLogging','logLevel') == "DEBUG":
            self.logLevel = logging.DEBUG
        elif configParserObj.get('CogentLogging','logLevel') == "INFO":
            self.logLevel = logging.INFO
        elif configParserObj.get('CogentLogging','logLevel') == "ERROR":
            self.logLevel = logging.ERROR
        elif configParserObj.get('CogentLogging','logLevel') == "CRITICAL":
            self.logLevel = logging.CRITICAL
        else:
            raise("Unknown Log Level provided")
        
        self.logger.setLevel(self.logLevel)
        
        # Build a log formatter #
        formatter = logging.Formatter('%(asctime)s : %(name)-32s : %(threadName)s : %(process)d : %(message)s')
        
        # Create file handler logger #
        log_location = configParserObj.get('CogentLogging','logPath')
        if os.path.isdir(log_location):
            log_file = os.path.realpath(os.path.realpath(log_location) + "/" + "CogentDigitGenerate.log")
        else:
            log_file = os.path.realpath(os.path.realpath(tempfile.gettempdir()) + "/" + "CogentDigitGenerate.log")
        print(datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + " : cogentDigitSequenceGenerator : Message : " + "Log File = " + log_file)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        fh.setLevel(self.logLevel)
        
        #ch = logging.StreamHandler()
        #ch.setLevel(self.logLevel)
        #ch.setFormatter(formatter)
        
        # register handlers with main logger obj #
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)
        
        self.logger.info("---- Started Logging Framework ----")
    def getLogger(self):
        return(self.logger)
        

# Build a singleton object here #
def __globalinit():
    return CogentLogging()

global CogentGlobalLoggingObj
CogentGlobalLoggingObj = __globalinit()