#!/usr/bin/env python

import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(message)s')
file_handler = logging.FileHandler('facefolder.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def timelogger(func):
    ''' Timing decorator for individual functions, logs to specified file '''
    def timeinner(*args, **kwargs):
        start = time.time()  # start time of the other function
        result = func(*args, **kwargs)  # this is the function
        end = time.time()  # end time of the other function
        report = (func.__name__ + ' took: ' + str((end-start) * 1000) +
                  ' milli seconds')
        funcn = func.__name__
        funcruntime = (funcn + " execution time: " + str((end-start) * 1000))
        logger.info(funcruntime)
        #print(report)
        return result  # return the other function to the inner function

    return timeinner  # return that to the outer function
