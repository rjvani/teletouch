
import socket
import ast
import RPi.GPIO as GPIO

UDP_IP = "128.237.130.27" #receiver's IP
UDP_PORT = 5005

def activate(data):
	#read from data dictionary and activate actuators with gpios
	return

def testActivate():
	#see if gpio pwm works
	GPIO.setmode(GPIO.BOARD)
	pin = 23
	GPIO.setup(pin, GPIO.OUT)
	p = GPIO.PWM(pin, 0.5)
	p.start(50)
	while (1):
		x = raw_input('Press a to stop:')   # use raw_input for Python 2
		#p.stop()
		if (x == "s"):
			pin = 24 if (pin==23) else 23
			p.stop()
			GPIO.cleanup()
			GPIO.setup(pin, GPIO.OUT)
			p = GPIO.PWM(pin, 0.5)
			p.start(50)
		elif (x=="a"):
			p.stop()
			GPIO.cleanup()
			break
	GPIO.cleanup()

def test():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18, GPIO.OUT)
	p = GPIO.PWM(18, 0.5)
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
        # activate(dataDict)

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

demoReceive()
