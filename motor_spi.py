#!/usr/bin/env python
import sys
import spidev

rotate = int(sys.argv[1])
cmd = rotate << 4
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 8000000
#spi.mode = 0b01
spi.xfer2([cmd])
spi.close()
