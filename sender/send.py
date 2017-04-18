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

"""
Read from individual expander pin
"""
def RCtime(mcp, RCpin):
    reading = 0
    mcp.config(RCpin, mcp.OUTPUT)
    GPIO.output(RCpin, 0)
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
    for x in range(0, 20):
        loopCount = 100
        tot = 0
        count = 0
        pinNum = x
        if (x >= 16):
            # use mcp 2 when done with 16 pins on mcp1
            mcp = mcp2
            pinNum = x % 16
        while (count < loopCount):
            tot += RCtime(mcp, pinNum)
            count ++
        avg = tot/loopCount
        DEFAULT_VALUES[chr(currSensor)] = avg
        THRESHOLD_VALUES[chr(currSensor)] = 8 # TODO: fine tune this
        currSensor ++

"""
Read from expanders and consolidate into dictionary
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
        diff = DEFAULT_VALUES[chr(currSensor)] - reading
        data[chr(currSensor)] =  0
        if (diff >= THRESHOLD_VALUES[chr(currSensor)]):
            # touched, scale to 100
            lowest = 8 #TODO: fine tune this, different lowest for different sensors?
            range = DEFAULT_VALUES[chr(currSensor)] - THRESHOLD_VALUES[chr(currSensor)] - lowest
            scaleFactor = 100/range
            data[chr(currSensor)] =  scaleFactor * (reading-lowest)
        currSensor ++
    return data

"""
calibrate and initiate connection, send data over
"""
def main():
	calibrate()
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while (1):
		data = sense()
		dataToSend = str(data)
		sock.sendto(dataToSend, (UDP_IP, UDP_Port))

main()

