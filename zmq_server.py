import zmq

context = zmq.Context()
socket = context.socket(
            zmq.REP)
socket.bind('tcp://*:1980')

while True:
    message = socket.recv()
    print message
    socket.send("I'm here")
