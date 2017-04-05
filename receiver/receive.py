# File: receive.py
# Authors: Rohan Jadvani, Chelsea Kwong, Cristian Vallejo, Lisa Yan
# Brief: Implementation of glove receiver code.

import socket
import ast
import RPi.GPIO as GPIO

# Size of buffer in bytes
BUFFER_SIZE = 1024
# Receiver's IP
UDP_IP = "128.237.195.168"
# Receiver port
UDP_PORT = 5005
# Current pins being used
CURR_PINS = [11, 12, 13, 15, 16, 18, 19, 21, 23]
# Mapping of pins to frequency
PIN_DICT = dict()
# Mapping of pin numbers to pin objects
PIN_OBJS = dict()
# mapping from dictionary to gpio pins
MAPPING = { 'A':[12, 16, 18], 'B':[11, 13, 15], 'C':[19, 21, 23]}

def activate(data):
    freq_factor = 70

    for key in data:
        for index in range(len(data[key])):
            pin_num = MAPPING[key][index]
            PIN_DICT[pin_num] = freq_factor * data[key][index]

    # Output all the frequency values
    for pin_num in PIN_OBJS:
        pin_obj = PIN_OBJS[pin_num]
        pin_freq = PIN_DICT[pin_num]
        pin_obj.ChangeFrequency(pin_freq + 1)
        pin_obj.start(50)

def parse(stringData):
    data = ast.literal_eval(stringData)
    return data

# Initializes and sets up all the necessary pins on the PI
# TODO: Add extra pins after PCB arrives
def gpio_init():
    # Use pin numbering
    GPIO.setmode(GPIO.BOARD)

    # Use PI interface to set up each pin
    for pin_num in CURR_PINS:
        GPIO.setup(pin_num, GPIO.OUT)
        # Initialize the frequency to be 0 Hz
        PIN_DICT[pin_num] = 70

        p = GPIO.PWM(pin_num, 1)
        PIN_OBJS[pin_num] = p

def receive():
    PREV_DICT = dict()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    gpio_init()
    # Constantly receive input and modify actuators
    while (1):
        data, addr = sock.recvfrom(BUFFER_SIZE)
        dataDict = parse(data)
        if dataDict != PREV_DICT:
            print "Received " + str(data)
            PREV_DICT = dataDict
            activate(dataDict)

receive()

