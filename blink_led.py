import time
from itertools import cycle
import RPi.GPIO as io

io.setmode(io.BCM)
io.setup(18, io.OUT)

o = cycle([1, 0])
while True:
    io.output(18, o.next())
    time.sleep(0.5)
