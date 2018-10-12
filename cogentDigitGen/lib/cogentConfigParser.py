from configparser import ConfigParser
import os

class CogentConfigParser(object):
    def __init__(self):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        self._configFileName = os.path.realpath(dirPath + "/../etc/config.ini")
        self.parser = self._readConfig()
        
    def _readConfig(self):
        try:
            parserObj = ConfigParser()
            parserObj.read(self._configFileName)
            return(parserObj)
        except Exception as e:
            raise(e)