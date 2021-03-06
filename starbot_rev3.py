#!/usr/bin/env python3

import logging
import platform
import subprocess
import sys

#Neopixel imports
import time
import board
import neopixel

pixel_pin = board.D12
num_pixels = 30
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts

#Matrix imports
import re
import time
import argparse
import luma

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

#Initializing Board
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#GPIO.setup(26, GPIO.OUT) #Servo 0
#GPIO.setup(6, GPIO.OUT) #Servo 1
#GPIO.setup(13, GPIO.OUT) #Servo 2
#GPIO.setup(5, GPIO.OUT) #Servo 3
#GPIO.setup(12, GPIO.OUT) #Servo 4
#GPIO.setup(24, GPIO.OUT) #Servo 5
#GPIO.setup(4, GPIO.OUT) #Driver 0
#GPIO.setup(17, GPIO.OUT) #Driver 1
#GPIO.setup(27, GPIO.OUT) #Driver 2
#GPIO.setup(22, GPIO.OUT) #Driver 3

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
print("Created device")

def printMatrix(msg):
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.017)
    
def printWTTS(msg):
    tts.say(msg)
    printMatrix(msg)

def power_off_pi():
    msg = 'Good bye!'
    printWTTS(msg)
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    msg = 'See you in a bit'
    printWTTS(msg)
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    msg = 'My IP address is %s' % ip_address.decode('utf-8')
    printWTTS(msg)

def led_on():
    msg = 'Turning LED on'
    printWTTS(msg)
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)

def led_off():
    msg = 'Turning LED off'
    printWTTS(msg)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)

def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'led on':
            assistant.stop_conversation()
            led_on()
        elif text == 'led off':
            assistant.stop_conversation()
            led_off()
        else:
            assistant.stop_conversation()
            tts('I do not know this one.  Please try again.')
            printMatrix(text)
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK  # Ready.
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()

