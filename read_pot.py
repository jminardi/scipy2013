import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

def readadc(adcnum):
    if not 0 <= adcnum <= 7:
        return -1
    r = spi.xfer2([1, (8+adcnum)<<4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

while True:
    val = readadc(3)
    print val
    time.sleep(0.5)
