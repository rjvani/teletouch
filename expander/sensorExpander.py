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
		print "Sensor: ", RCtime(0)
	except KeyboardInterrupt:
		sys.exit()
