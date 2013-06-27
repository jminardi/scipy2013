import time
import json
import os
import threading

import spidev
import zmq

from robot_brain.servo import Servo

SERVO = Servo(pin=0, min=60, max=200)

spi = spidev.SpiDev()
spi.open(0,0)

class SensorServer(object):

    def __init__(self, port=2022):
        self.port = port

        # Whether or not to continue running the server
        self._run = True

        self.sensor_data = {}

        self.start()

    def start(self):
        """ Initialize and start threads. """

        self._server_thread = threading.Thread(target=self._server_worker)
        self._server_thread.start()

        self.acc_thread = threading.Thread(target=self._read_worker)
        self.acc_thread.start()

    def stop(self):
        """ Shut down server and control threads. """
        self._run = False
        self._server_thread.join()
        self.acc_thread.join()

    def _server_worker(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.port))
        print 'bound to socket:', socket, self.port

        while self._run:
            time.sleep(.1)
            #  Wait for next request from client
            message = socket.recv()
            print "Received request: ", message

            #  Send current sensor values back to client
            socket.send(json.dumps(self.sensor_data))
        socket.close()

    def _read_worker(self):
        x_pin = 0
        y_pin = 1
        z_pin = 2

        while self._run:
                # read the analog pins
                x_val = readadc(x_pin)
                y_val = readadc(y_pin)
                z_val = readadc(z_pin)
                self.sensor_data['acc_x'] = x_val
                self.sensor_data['acc_y'] = y_val
                self.sensor_data['acc_z'] = z_val
                time.sleep(0.1)


def readadc(adcnum):
    """ read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7).  """

    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1,(8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout
