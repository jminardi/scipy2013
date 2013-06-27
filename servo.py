import time
import numpy as np
from robot_brain.servo import Servo

servo = Servo(pin=0, min=60, max=200)

for val in np.arange(0, 1, 0.05):
    servo.set(val)
    time.sleep(0.1)
