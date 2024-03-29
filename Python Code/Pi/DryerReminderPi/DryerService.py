""" DryerService which acts as a service to access the Dryer
section of the library

Author: Michael Mohler
Data: 12/26/21
Version: 1
"""

import logging
import logging.handlers as handlers
import DryerLibrary
import AxesModel


#Logging Configure
logging.basicConfig(filename='dryer.log',
    format='%(asctime)s-%(levelname)s-%(message)s', level=logging.DEBUG)
logger = logging.getLogger('DryerService')
logHandler = handlers.RotatingFileHandler('dryer.log', maxBytes=1000000, backupCount=1)
logger.addHandler(logHandler)

class DryerService:
    """Shake Detection Service to be used as an inbetween for the api and library"""

    def dryer_check(saved_range):
        """Calls the library service with the saved ranges.
        I would like to move the offset here later

        Arg: saved_range Range of the Pi when not moving
        """

        logging.debug("Start - Dryer Service")
        DryerLibrary.justMain(saved_range)
        logging.debug("End - Dryer Service")

    if __name__ == '__main__':
        axes = AxesModel.AxesModel(1, 1, 1)
        dryer_check(axes)
