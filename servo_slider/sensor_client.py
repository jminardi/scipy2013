import json
import threading

import enaml
import zmq

from io_controller import IOController


class SensorApp(object):

    def __init__(self, ip='192.168.43.186', port=2026):
        self.ip = ip
        self.port = port
        self._run = True
        self.io_controller = IOController()

        self.start()

    def start(self):
        self._run = True
        self._sensor_client_thread = threading.Thread(
                target=self._sensor_client_worker)
        self._sensor_client_thread.start()

    def stop(self):
        self._run = False

    def _sensor_client_worker(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(self.ip, self.port))
        print 'connected to:', self.ip, self.port

        while self._run:
            send = {'servo': self.io_controller.servo_value}
            socket.send(json.dumps(send))
            message = socket.recv()
            print 'received:', message
        socket.close()


if __name__ == '__main__':
    from enaml.stdlib.sessions import show_simple_view
    with enaml.imports():
        from sensor_view import SensorViewWindow
    sensor_app = SensorApp()
    window = SensorViewWindow(io_controller=sensor_app.io_controller)
    show_simple_view(window)
    sensor_app.stop()
