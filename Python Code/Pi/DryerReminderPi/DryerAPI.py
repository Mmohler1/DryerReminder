""" The API that will be used to control the Services on the Raspberry Pi Application.
There will be 3 to 4 URL's for controling the adjust, calibrating, and dryer/washer service.
Flask is used to setup these URL's. Jsonify is used to sent data over the API. Make_Response allows
for the program to define which response status code is sent.

Author: Michael Mohler
Data: 12/07/21
Version: 1
"""
#import time
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api


import DryerLibrary
import DryerService
#import WasherService
import AxesModel


#Intialize the varaibles for handling the ipAddress, port, and the sercurity token.
IPADDRESS = '192.168.0.23'
PORT = "7069"
TOKEN = ""

#Defines the service to run and API's to start.
app = Flask(__name__)
api = Api(app)



class Dryer(Resource):
    """Dryer Class for starting the dryer process after taking in the saved AxesModel values
    Returns a response status code to let the user know when thier dryer has stopped moving"""

    @classmethod
    def post(cls):
        """Post for Dryer

        Return: JSON and Response status"""

        print("Start - Dryer API")

        try:
            #JSON data is pulled which contains the saved ranges of each axis
            json_data = request.get_json()
            axis_x = json_data['axisX']
            axis_y = json_data['axisY']
            axis_z = json_data['axisZ']


            axes = AxesModel.AxesModel(axis_x, axis_y, axis_z)

            #The dryer service is called with which saved range to use
            DryerService.DryerService.dryerCheck(axes)

            print("End - Dryer API")
            return make_response(jsonify(axes.to_json()), 200)
        except TypeError:
            return make_response("Invalid input, object was invalid", 400)
        except:
            return make_response("System Error", 500)


class Washer(Resource):
    """Washer Class for starting the Washer process after taking in the saved AxesModel values
    Returns a response status code to let the user know when thier washer has stopped moving"""

    @classmethod
    def post(cls):
        """Post for Washer

        Return: JSON and Response status"""

        print("Start - Washer API")
        #WasherService.washerCheck()
        print("End - Washer API")
        return  make_response("Washer", 200)


class Calibrate(Resource):
    """#Calibrate the accelerometer by saving the axes and sending the results back over JSON
    Returns a response status code and JSON of the Axes model"""

    @classmethod
    def post(cls):
        """Post for Calibrate

        Return: JSON and Response status"""

        print("Start - Calibrate API")

        #Try to call the calibrate service and return the range
        try:
            #This will return an axes model of the range for when the device is not moving
            axes = DryerLibrary.calibrate()

            print("End - Calibrate API")
            return make_response(jsonify(axes.to_json()), 200) #Returns the axes in JSON
        except:
            return make_response("Error", 400)   #An error has happened


class Adjust(Resource):
    """Update the offset to better detect when the device is or is not moving.
    Returns a response status code"""

    @classmethod
    def post(cls):
        """Post for Adjust

        Return: JSON and Response status"""

        print("Start - Adjust API")

        #DryerLibrary.setOffset()

        print("End - adjust API")
        return make_response("Adjust", 200)


#A class will be called depending on the URI that was called over the service
api.add_resource(Dryer, '/DryPi/dryStop')
api.add_resource(Washer, '/DryPi/washerStop')
api.add_resource(Calibrate, '/DryPi/calibrate')
api.add_resource(Adjust, '/DryPi/adjust')



#Runs the service when started, defines the host and port.
if __name__ == '__main__':
    app.run(debug=True, host=IPADDRESS, port=PORT)
