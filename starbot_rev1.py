#Neopixel imports
import time
import board
import neopixel

#Matrix imports
import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

#Assistant imports
import logging
import platform
import subprocess
import sys

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts

#Initializing Board
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(26, GPIO.OUT) #Servo 0
GPIO.setup(6, GPIO.OUT) #Servo 1
GPIO.setup(13, GPIO.OUT) #Servo 2
GPIO.setup(5, GPIO.OUT) #Servo 3
GPIO.setup(12, GPIO.OUT) #Servo 4
GPIO.setup(24, GPIO.OUT) #Servo 5

GPIO.setup(4, GPIO.OUT) #Driver 0
GPIO.setup(17, GPIO.OUT) #Driver 1
GPIO.setup(27, GPIO.OUT) #Driver 2
GPIO.setup(22, GPIO.OUT) #Driver 3

#Create Neopixel Strip for Head
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D12
num_pixels = 80
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)





