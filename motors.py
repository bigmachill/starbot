#!/usr/bin/env python
import sys
import spidev
import time

def send_motor_speed(speed):
  speed = int(speed)
  spi = spidev.SpiDev()
  spi.open(0,1)
  spi.max_speed_hz = 8000000
  spi.xfer2([speed << 4])
  time.sleep(0.1)
  spi.xfer2([speed << 4])
  spi.close()
