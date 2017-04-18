import RPi.GPIO as GPIO, time, os
import sys
from Adafruit_MCP230xx import *

"""
Read sensor from expander
"""

mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017

def RCtime(RCpin):
	reading = 0
	mcp.config(RCpin, mcp.OUTPUT)
	mcp.output(RCpin,0)
	time.sleep(0.05)

	mcp.config(RCpin, mcp.INPUT)
	while(mcp.input(RCpin) == 0):
		reading += 1
	return reading

while True:
    try:
    	reading = RCtime(2)
    	print "Sensor: ", reading
        defaultValue = 164
        threshold = 10
        lowest = 80
        if (reading < lowest):
        	print "100"
        elif (reading < defaultValue - threshold):
        	range = defaultValue - threshold - lowest
        	scaleFactor = 100/range
        	print str(scaleFactor * (defaultValue - threshold - reading) + 1)
    except KeyboardInterrupt:
        sys.exit()
