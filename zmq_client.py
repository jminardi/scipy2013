import zmq

context = zmq.Context()
socket = context.socket(
    zmq.REQ)
a = 'tcp://192.168.1.68:1980'
socket.connect(a)

for request in range(10):
    socket.send('You home?')
    message = socket.recv()
    print message
