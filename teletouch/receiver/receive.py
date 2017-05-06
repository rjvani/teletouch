# File: receive.py
# Authors: Rohan Jadvani, Chelsea Kwong, Cristian Vallejo, Lisa Yan
# Brief: Implementation of glove receiver code.

from pymongo import MongoClient
import Adafruit_PCA9685
import requests
import datetime
import socket
import os
import ast
import RPi.GPIO as GPIO

# Vanity Sake
PREFIX = 'teletouch > '
# MONGODB_URI
MONGODB_URI = 'mongodb://heroku_w9j2glws:92r5t59p5go4givqetb7vhi34p@ds131151.mlab.com:31151/heroku_w9j2glws'
# TABLE
COLLECTION = "ip"
# Size of buffer in bytes
BUFFER_SIZE = 1024
# Receiver port
UDP_PORT = 5005
# Mapping of pins to frequency
PIN_DICT = dict()
# Mapping of pin numbers to pin objects
PIN_OBJS = dict()
# mapping from dictionary to gpio pins
MAPPING = {
        'A':[38, 15, 36, 33, 35],
        'B':[31, 32, 29, 12, 11],
        'C':[13, 22, 7, 16, 18],
        'D':[15, 40, 3, 12, 0] # CHANNEL 15, 3, 12, 0
    }
# Servo SERVO_CTRL.object
SERVO_CTRL = Adafruit_PCA9685.PCA9685()

# SERVO_CTRL.DRIVER DEF
ON = 0
OFF = 4095

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
    #data = ast.literal_eval(stringData)
    #return data
    data = [0,25,50,75,100]
    hand = {
            'A': data,
            'B': data,
            'C': data,
            'D': data
            }   # CHANNEL 15, 3, 12, 0
    return hand

# Initializes and sets up all the necessary pins on the PI
def gpio_init():
    # Teletouch never breaks
    GPIO.setwarnings(False)

    # Use pin numbering
    GPIO.setmode(GPIO.BOARD)

    for key in MAPPING:
        if ( key == 'D' ):
            pin_init(MAPPING[key][1])
        else:
            for pin in MAPPING[key]:
                pin_init(pin)

def pin_init(pin):
    print PREFIX, 'Setting up pin '+str(pin)+'...',
    GPIO.setup(pin, GPIO.OUT)
    # Initialize the frequency to be 0 Hz
    PIN_DICT[pin] = 0

    pin_obj = GPIO.PWM(pin, 1)
    PIN_OBJS[pin] = pin_obj
    print 'Done.'

# Assuming sensors give val [0,100]
def get_freq(val, mode):
    min_freq = 150
    if ( val == 0 and mode == "GPIO"):
        return 0
    elif ( val == 0 and mode == "CHANNEL"):
        return 4096
    return min_freq + val

def vibrate_hand(data):
    # Save frequency to output
    for key in data:
        for i in xrange(len(data[key])):
            pin_num = MAPPING[key][i]
            sensor_val = data[key][i]
            if (key == 'D' and i != 1):
                PIN_DICT['CH'+str(pin_num)] = get_freq(sensor_val, 'CHANNEL')
            else:
                PIN_DICT[pin_num] = get_freq(sensor_val, 'GPIO')

    """
    # Output all the frequency values
    for pin_num in PIN_OBJS:
        pin_obj = PIN_OBJS[pin_num]
        pin_freq = PIN_DICT[pin_num]
        pin_obj.ChangeFrequency(pin_freq + 1)
        pin_obj.start(50)
    """

    for j in xrange(len(MAPPING['D'])):
        if (j == 1): #skip the GPIO pin
            continue
        channel = MAPPING['D'][j]
        channel_freq = PIN_DICT['CH'+str(channel)]
        SERVO_CTRL.set_pwm_freq(channel_freq)
        SERVO_CTRL.set_pwm(channel, ON, OFF)

def receive():
    print PREFIX, 'Waking up the API... ',
    r = requests.get('http://teletouch.herokuapp.com/api/wake')

    if ( r.status_code == requests.codes.ok ):
        print 'Done.'
    else:
        return

    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    ip_collection = db[COLLECTION]

    print PREFIX, 'Cleaning UDP_IP from collection...'
    ip_collection.remove()

    ip = getIP()

    ip_post = {
                "ip": ip,
                "createDate": datetime.datetime.utcnow()
              }

    result = ip_collection.insert(ip_post)

    if (result != None):
        print PREFIX, 'POST UDP_IP: '+ip+' succeeded. Sender will GET proper UDP_IP.'
    else:
        print PREFIX, 'POST request failed. Sender will not GET proper UDP_IP'
        return

    PREV_DICT = dict()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((getIP(), UDP_PORT))
    gpio_init()

    data = None

    print PREFIX, 'Receiving on UDP_PORT '+str(UDP_PORT)+'...'

    # Constantly receive input and modify actuators
    while (1):
        #data, addr = sock.recvfrom(BUFFER_SIZE)
        dataDict = parse(data)
	vibrate_hand(dataDict)
        # if dataDict != PREV_DICT:
        #     print PREFIX, "Received " + str(data)
        #     PREV_DICT = dataDict
        #     activate(dataDict)

if __name__ == "__main__":
    receive()
