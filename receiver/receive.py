# File: receive.py
# Authors: Rohan Jadvani, Chelsea Kwong, Cristian Vallejo, Lisa Yan
# Brief: Implementation of glove receiver code.

import socket
import ast
import RPi.GPIO as GPIO

# Size of buffer in bytes
BUFFER_SIZE = 1024
# Receiver's IP
UDP_IP = "128.237.177.230"
# Receiver port
UDP_PORT = 5005
# Current pins being used
CURR_PINS = [7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40]
# Mapping of pins to frequency
PIN_DICT = dict()
# Mapping of pin numbers to pin objects
PIN_OBJS = dict()
# mapping from dictionary to gpio pins
MAPPING = { 
        'A':[7, 11, 0, 0, 0], 
        'B':[0, 13, 0, 12, 0], 
        'C':[15, 16, 0, 18, 0], 
        'D':[0, 22, 29, 0, 0],
        'E':[31, 32, 0, 0, 0], 
        'F':[33, 35, 0, 0, 0], 
        'G':[36, 37, 0, 0, 0], 
        'H':[38, 40, 0, 0, 0] 
    }

# FRONT / BACK
# A/E: Thumb tip, Index tip
# B/F: Middle tip, Ring tip
# C/G: Pinky tip, Top left palm
# D/H: Top right palm, Bottom left palm, Bottom right palm

def activate(data):
    lo = 100

    for key in data:
        for index in range(len(data[key])):
            pin_num = MAPPING[key][index]
            factor = data[key][index]
            if factor == 0:
                PIN_DICT[pin_num] = 0
            else:
                PIN_DICT[pin_num] = lo + 40 * factor

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
        PIN_DICT[pin_num] = 0

        p = GPIO.PWM(pin_num, 1)
        PIN_OBJS[pin_num] = p

def vibrateHand(data):
    temp_dict = { 'A': 12, 'B': 16, 'C': 18, 'D': 22 }	
    off_vals = {'A': 43, 'C': 43, 'B': 20, 'D': 20}
    # Minimum frequency difference
    threshold = 100
    max_freq_factor = 300

    # Save frequency to output
    for key in data:
	pin_num = temp_dict[key]
	sensor_val = data[key]
	new_freq = max_freq_factor * (off_vals[key] - sensor_val) / off_vals[key]
	# Sensor is being touched at this location
	if new_freq > threshold:
	    PIN_DICT[pin_num] = new_freq
	else:
	    PIN_DICT[pin_num] = 0

    # Output all the frequency values
    for pin_num in PIN_OBJS:
        pin_obj = PIN_OBJS[pin_num]
        pin_freq = PIN_DICT[pin_num]
        pin_obj.ChangeFrequency(pin_freq + 1)
        pin_obj.start(50)

def receive():
    PREV_DICT = dict()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    gpio_init()
    # Constantly receive input and modify actuators
    while (1):
        data, addr = sock.recvfrom(BUFFER_SIZE)
        dataDict = parse(data)
	vibrateHand(dataDict)
        # if dataDict != PREV_DICT:
        #     print "Received " + str(data)
        #     PREV_DICT = dataDict
        #     activate(dataDict)

receive()

