import time
import json
import threading

import zmq

from robot_brain.servo import Servo

SERVO = Servo(pin=0, min=60, max=200)


class SensorServer(object):

    def __init__(self, port=2022):
        self.port = port

        # Whether or not to continue running the server
        self._run = True

        self.start()

    def start(self):
        """ Initialize and start threads. """

        self._server_thread = threading.Thread(target=self._server_worker)
        self._server_thread.start()

    def stop(self):
        """ Shut down server and control threads. """
        self._run = False
        self._server_thread.join()

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

            request = json.loads(message)
            SERVO.set(request['servo'] / 100.0)
            socket.send('REP')
        socket.close()
