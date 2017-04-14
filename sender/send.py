import socket
import RPi.GPIO as GPIO, time, os
GPIO.setmode(GPIO.BCM)
UDP_IP = "128.237.177.230" #receiver's IP
UDP_Port = 5005
MSG = 'heloo'
# DEFAULT_VALUES_DICT = dict([('A', [0,0,0,0,0]),
#                         ('B', [0,0,0,0,0]),
#                         ('C', [0,0,0,0,0]),
#                         ('D', [0,0,0,0,0]),
#                         ('E', [0,0,0,0,0]),
#                         ('F', [0,0,0,0,0]),
#                         ('G', [0,0,0,0,0]),
#                         ('H', [0,0,0,0,0])])

DEFAULT_VALUES_DICT = dict( [ ('A',0), ('B', 0), ('C',0), ('D',0)])

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
	data = dict()
	data['A'] = RCtime(24)
    data['B'] = RCtime(23)
    data['C'] = RCtime(25)
    data['D'] = RCtime(22)
    return data

def main():
	calibrate()
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while (1):
		data = sense()
		dataToSend = str(data)
		sock.sendto(dataToSend, (UDP_IP, UDP_Port))

main()

