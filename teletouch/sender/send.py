import socket
import RPi.GPIO as GPIO, time, os
GPIO.setmode(GPIO.BCM)
UDP_IP = "128.237.177.230" #receiver's IP
UDP_Port = 5005
MSG = 'heloo'

def RCtime(RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.05)

    GPIO.setup(RCpin, GPIO.IN)
    while(GPIO.input(RCpin) == GPIO.LOW):
        reading +=1
    return reading

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
	return test

def send():
	#constantly sending to receiver pi
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print "Sending..."
	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_Port
	print 'message:',MSG
	while (1):
		#data = sense()
                dic = dict()
                dic['A'] = RCtime(24)
                dic['B'] = RCtime(23)
                dic['C'] = RCtime(25)
                dic['D'] = RCtime(22)
                dataToSend = str(dic)
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

#demoSend()
send()

