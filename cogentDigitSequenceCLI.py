# Cogent Digit Sequence Generator CLI #

import os
import sys
import traceback
import argparse
from datetime import datetime
import json

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
            package_dir = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(package_dir)
        os.chdir(package_dir)
    except Exception as e:
        printStdOutMessage("Unable to setup locations, exception : %s" %(str(e)))
        raise(e)
   
def startProgram():
    """
    Function for starting the program.
    Image data and image label information to read from config. In case customized image data is to be used, update the config file
    
    Args : <None>
    Output : <None>
    """
    try:
        __setupLocations()
        # For testing #        
        #__setupLocations("C:\\Users\\anugraha.sinha\\OneDrive\\Documents\\Cogent\\mnist_digit_seq_gen")
        from cogentDigitGen.lib import CogentUtils
        utilObj = CogentUtils()
        options = utilObj.parseCLIArguments()
        if not options:
            return False,"Problem with parsing CLI arguments"
        
        from cogentDigitGen.lib import CogentDigitGenerateSequence
        from cogentDigitGen.lib import CogentDigitGenerateReadImageData
        obj = CogentDigitGenerateSequence(CogentDigitGenerateReadImageData,**options)
        obj.execute()
        # dump the image present in the object #
        dumpFileName = utilObj.dumpImage(options["outputPath"],obj.outputImageArray,obj.imageMetaInfo)
        if dumpFileName:
            outputData = obj.imageMetaInfo
            outputData["filename"] = dumpFileName
            return(True,"Execution completed successfully\n%s" %(str(json.dumps(outputData,indent=2))))
        else:
            return(False,"Unable to complete execution, check log files")
    except Exception as e:
        printStdOutMessage("Program received exception, check log file. Exception summary : %s" %(str(e)))
        # testing #
        printStdOutMessage("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))
        return(False,"There was a problem in executing the program : %s" %(str(e)))
        # Do not raise an exception, as the problem is related to program execution, log file should be checked

if __name__ == "__main__":
    """
    Main function for starting the CLI
    
    Args : <TBD>
    Output : <TBD>
    """
    try:
        executionResult, message = startProgram()
        if executionResult:
            printStdOutMessage(message)
            sys.exit(0)
        else:
            printStdOutMessage("Execution Failed, with message : %s" %(message))
            sys.exit(127)
    except Exception as e:
        printStdOutMessage("Unable to start program : Exception : %s\n%s" %(str(e),"\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ])))
        sys.exit(127)