#!/usr/bin/env python3

import logging
import platform
import subprocess
import sys

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

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
print("Created device")


#Initialize GPIO ports
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT) #Drivers 1
GPIO.setup(6, GPIO.OUT) #Drivers 2
GPIO.setup(13, GPIO.OUT) #Drivers 3

logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def printMatrix(msg):
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.017)


def power_off_pi():
    tts.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    tts.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))
    
def led_on():
    tts.say('Turning LED on')
    printMatrix('Turning LED on')
    GPIO.output(26, GPIO.HIGH)
    
def led_off():
    tts.say('Turning LED off')
    printMatrix('Turning LED off')
    GPIO.output(26, GPIO.LOW)


def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready to accept commands.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Put code to demonstrate listening
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        printMatrix(text)
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
        elif text == 'goodbye':
            assistant.stop_conversation()
            tts.say('See you later allegator!')
        elif text == 'see you later allegator!':
            assistant.stop_conversation()
            tts.say('In a while crocodile!')
            
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK  # Ready to receive input.
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