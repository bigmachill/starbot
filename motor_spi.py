#!/usr/bin/env python
import sys
import spidev
import time

cmd = int(sys.argv[1])
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 8000000
spi.mode = 0b01
spi.xfer2([cmd])
time.sleep(0.1)
spi.xfer2([cmd])
spi.close()
