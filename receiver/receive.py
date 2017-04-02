#
# GPIO pin numbers are actual pin numbers, not BCM pins
#

import socket
import ast
import RPi.GPIO as GPIO

UDP_IP = "128.237.208.146" #receiver's IP, change every time connect to wifi
UDP_PORT = 5005
# mapping from dictionary to gpio pins
MAPPING = { 'A':[12, 16, 18], 'B':[11, 13, 15], 'C':[19, 21, 23]}

def activate(data):
	#make map from pin number to intensity,
	#read from data dictionary and activate actuators with gpios
	pinToFrequency = {}
	dictIndices = ['A','B','C']
	#get intensity values from dictionary received
	for x in range(3):
		index = dictIndices[x]
		for y in range(3):
			value = data[y]
			if ((value != 0) && (value <=3)):
				freq = 70 * value #70hz, 140hz, 210hz
				pinNum = MAPPING[index][y]
				pinToFrequency[pinNum] = freq
	#activate actuators
	GPIO.setmode(GPIO.BOARD)
	allPins = []
	#set up all pins 
	for key in pinToFrequency:
		GPIO.setup(key, GPIO.OUT)
		p = GPIO.PWM(key, 0.5)
		p.ChangeFrequency(pinToFrequency[key])
		allPins.append(p)

	for pin in allPins:
		pin.start(50)

	input('Press return to stop:')

	for stopPins in allPins:
		stopIns.stop()

	GPIO.cleanup()
	return

def test():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18, GPIO.OUT)
	p = GPIO.PWM(18, 0.5)
	p.ChangeFrequency(200)
	p.start(50)
	input('Press return to stop:')   # use raw_input for Python 2
	p.stop()
	GPIO.cleanup()

def parse(stringData):
	#parse received string into dictionary form
	# testStr = "{'A': [1, 2, 3, 4, 5], 'C': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], 'E': [1, 2, 3, 4, 5], 'D': [1, 2, 3, 4, 5], 'G': [1, 2, 3, 4, 5], 'F': [1, 2, 3, 4, 5], 'H': [1, 2, 3, 4, 5]}"
	data = ast.literal_eval(stringData)
	return data

def receive():
	#constantly receiving and updating actuators	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
	while (1):
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "received message:",data
        dataDict = parse(data)
        activate(dataDict)

def demoReceive():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
	GPIO.setmode(GPIO.BOARD)
	pin = 16
	GPIO.setup(pin, GPIO.OUT)
	p = GPIO.PWM(pin, 0.5)
	p.ChangeFrequency(200)
	p.start(50)
	while (1):
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "received message:",data
		if (data == "s"):
			pin = 18 if (pin==16) else 16
			p.stop()
			GPIO.cleanup()
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			p = GPIO.PWM(pin, 0.5)
			p.ChangeFrequency(200)
			p.start(50)
		elif (data=="a"):
			p.stop()
			GPIO.cleanup()
			break
	# GPIO.cleanup()

receive()
