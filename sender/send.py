from Adafruit_MCP230xx import *
import socket
import RPi.GPIO as GPIO, time, os

"""
Global variables
"""
UDP_IP = "128.237.177.230" #receiver's IP
UDP_Port = 5005
mcp1 = Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017
mcp2 = Adafruit_MCP230XX(address = 0x21, num_gpios = 16) # MCP23017
DEFAULT_VALUES = dict() # default values of sensors when untouched
THRESHOLD_VALUES = dict() # threshold difference to activate actuator
LOWEST_VALUES = dict()
"""
Read from individual expander pin
"""
def RCtime(mcp, RCpin):
    reading = 0
    mcp.config(RCpin, mcp.OUTPUT)
    #GPIO.output(RCpin, 0)
    time.sleep(0.05)

    mcp.config(RCpin, mcp.INPUT)
    while(mcp.input(RCpin) == 0):
        reading +=1
    return reading

"""
Go through all sensors and grab the default vals
TODO: fine tune threshold values and min nums when pressed
"""
def calibrate():
    # mcp 1: pins 0 thru 15
    # mcp2: pins 0 thru 3
    mcp = mcp1
    currSensor = ord('A')
    print "Calibrate"
    for x in range(0, 20):
        print "Calibrating sensor ", x+1, "..."
        if (x==0 or x==6 or x==8):
            currSensor += 1
            continue
        loopCount = 20
        tot = 0
        count = 0
        pinNum = x
        if (x >= 16):
            # use mcp 2 when done with 16 pins on mcp1
            mcp = mcp2
            pinNum = x % 16
        while (count < loopCount):
            tot += RCtime(mcp, pinNum)
            count += 1
        avg = tot/loopCount
        print avg
        DEFAULT_VALUES[chr(currSensor)] = avg
        THRESHOLD_VALUES[chr(currSensor)] = 8 # TODO: manual tune
        LOWEST_VALUES[chr(currSensor)] = 50 #TODO: manual tune
        currSensor += 1
    print "Done."


def printDefVals():
    currSensor = ord('A')
    for x in range(0, 20):
        if (x==0 or x==6 or x==8):
            continue
        print str(x), chr(currSensor+x), ": ", DEFAULT_VALUES[chr(currSensor+x)]



"""
Read from expanders, compute, and consolidate into dictionary
"""
def sense():
    data = dict()
    mcp = mcp1
    currSensor = ord('A')
    for x in range(0,20):
        pinNum = x
        if (x >= 16):
            mcp = mcp2
            pinNum = x % 16
        reading = RCtime(pinNum)
        threshold = THRESHOLD_VALUES[chr(currSensor)]
        lowest = LOWEST_VALUES[chr(currSensor)]
        default = DEFAULT_VALUES[chr(currSensor)]
        data[chr(currSensor)] =  0
        if (reading < lowest):
            data[chr(currSensor)] =  100
        elif (reading < default - threshold):
            # touched, scale to 100
            range = default - threshold - lowest
            scaleFactor = 100/range
            data[chr(currSensor)] =  scaleFactor * (default - threshold - reading) + 1
        currSensor += 1
    return data

"""
calibrate and initiate connection, send data over
"""
def main():
    calibrate()
    printDefVals()
	#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#while (1):
	#	data = sense()
	#	dataToSend = str(data)
	#	sock.sendto(dataToSend, (UDP_IP, UDP_Port))

GPIO.setmode(GPIO.BOARD)
main()

