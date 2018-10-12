# Basic imports #
import os
import sys
from datetime import datetime
import traceback
import logging

# Sanic imports #
from sanic import Sanic
from sanic.response import json
from sanic.response import json_dumps

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Project specific imports #
from cogentDigitGen.lib import CogentDigitGenerateSequence
from cogentDigitGen.lib import CogentDigitGenerateReadImageData
from cogentDigitGen.lib import CogentLogging
from cogentDigitGen.lib import CogentUtils

logger = logging.getLogger("CogentDigitBase.RESTServer")

app = Sanic()

usage = {"INFO" : "Help on usage of request string",
         "BASE_URL" : "<IP>:8080/cogentDigitGen?",
         "VALID QUERY STRINGS" : {
             "digits" : "Eg. [0,1,2,3,4] -> DEFAULT = [0,1,2,3,4,5,6,7,8,9] -> (** REQUIRED **)",
             "imageWidth" : "Eg. 1000 -> DEFAULT = 1000 -> (** OPTIONAL **)",
             "spacingRange" : "Eg. (0,100) -> DEFAULT = (0,100) -> (** OPTIONAL **)",
             "spacingMode" : "Eq. [EQUALIZED_MAX | EQUALIZED_MIN | PROGRESSIVE ] -> DEFAULT = EQUALIZED_MAX -> (** OPTIONAL **)"},
         }

@app.route("/")
def rootRoute(request):
    try:
        logger.debug("Root Route : Information received from %s is : %s" %(str(request.ip),str(request.raw_args)))
        return json(body={"ERROR" : "Invalid request for REST server",
                          "USAGE" : usage},
                        content_type = 'application/json',
                        dumps=json_dumps,
                        status=400,
                        indent=2)
    except Exception as e:
        logger.error("Some error with no route function, exception : %s" %(str(e)))
        logger.error("Exception Traceback :\n%s" %("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ])))
        # No raise here #

@app.route("/cogentDigitGen")
def handleRequest(request):
    try:
        if len(request.raw_args.keys()) > 0 and "digits" in request.raw_args.keys():
            logger.debug("cogentDigitGen Route : Information received from %s is : %s" %(str(request.ip),str(request.raw_args)))
            obj = CogentDigitGenerateSequence(CogentDigitGenerateReadImageData,**request.raw_args)
            obj.execute()
            s3_dump_location = CogentUtils().dumpImageAWS(obj.outputImageArray,obj.imageMetaInfo)
            return json(body={"imageMetaInfo" : obj.imageMetaInfo,"accessLocation" : s3_dump_location},
                        content_type='application/json',
                        dumps=json_dumps,
                        status=200,
                        indent=2)
        else :
            error = "REST URL used required arguments"
            raise(Exception(error))
    except Exception as e:
        logger.error("There was an exception in executing the request : %s" %(str(e)))
        logger.error("Exception Traceback :\n%s" %("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ])))
        return json(body={"ERROR" : str(e),
                          "USAGE" : usage},
                    content_type = 'application/json',
                    dumps=json_dumps,
                    status=400,
                    indent=2)

if __name__ == "__main__":
    logger.info("Starting with Cogent Digit Sequence Rest Server")
    app.run(host="0.0.0.0",port=8080)
    
    