# File: receive.py
# Authors: Rohan Jadvani, Chelsea Kwong, Cristian Vallejo, Lisa Yan
# Brief: Implementation of glove receiver code.

from pymongo import MongoClient
import datetime
import socket
import os
import ast
import RPi.GPIO as GPIO

# MONGODB_URI
MONGODB_URI = 'mongodb://heroku_w9j2glws:92r5t59p5go4givqetb7vhi34p@ds131151.mlab.com:31151/heroku_w9j2glws'
# TABLE
COLLECTION = "ip"
# Size of buffer in bytes
BUFFER_SIZE = 1024
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
        'A':[20, 22, 16, 13, 19],
        'B':[6, 12, 5, 18, 17],
        'C':[0, 25, 4, 23, 24],
        'D':[21, 0, 0, 0, 0]
    }

# FRONT / BACK
# A/E: Thumb tip, Index tip
# B/F: Middle tip, Ring tip
# C/G: Pinky tip, Top left palm
# D/H: Top right palm, Bottom left palm, Bottom right palm

def getIP():
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    ipaddr = s.getsockname()[0]
    return ipaddr

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
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    ip_collection = db[COLLECTION]

    print 'Cleaning UDP_IP from collection...'
    ip_collection.remove()

    ip = getIP()

    ip_post = {
                "ip": ip,
                "createDate": datetime.datetime.utcnow()
              }

    result = ip_collection.insert(ip_post)

    if (result != None):
        print 'POST UDP_IP: '+ip+' succeeded. Sender will GET proper UDP_IP.'
    else:
        print 'POST request failed. Sender will not GET proper UDP_IP'

    PREV_DICT = dict()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((getIP(), UDP_PORT))
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

if __name__ == "__main__":
    receive()
