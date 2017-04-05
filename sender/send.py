import socket
import RPi.GPIO as GPIO, time, os

UDP_IP = "128.237.208.146" #receiver's IP
UDP_Port = 5005
MSG = 'heloo'

def sense():
	#read from gpio headers and consolidate into dictionary
	# just a dummy dictionary placeholder
	test = dict([('A', [1,2,3,4,5]),
                        ('B', [1,2,3,4,5]),
                        ('C', [1,2,3,4,5]),
                        ('D', [1,2,3,4,5]),
                        ('E', [1,2,3,4,5]),
                        ('F', [1,2,3,4,5]),
                        ('G', [1,2,3,4,5]),
                        ('H', [1,2,3,4,5])])
	reading = 0
	GPIO.setup(18, GPIO.OUT)
	GPIO.output(18, GPIO.LOW)
	time.sleep(0.1)
	GPIO.setup(18, GPIO.IN)
	while(GPIO.input(18) == GPIO>LOW):
		reading += 1
	return reading
	#return test

def send():
	#constantly sending to receiver pi
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print "Sending..."
	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_Port
	print 'message:',MSG
	while (1):
		data = sense()
		print data
		dataToSend = str(data)
		sock.sendto(dataToSend, (UDP_IP, UDP_Port))

def demoSend():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print "Sending..."
	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_Port
	print 'message:',MSG
	data = "b"
	while (1):
		x = raw_input('Press s to switch and a to stop:')
		if (x == "s"):
			data = "s"
		elif (x=="a"):
			data = "a"
		sock.sendto(data, (UDP_IP, UDP_Port))

demoSend()

