import socket
import ast

UDP_IP = "172.20.10.21" #receiver's IP
UDP_PORT = 5005

def activate(data):
	#read from data dictionary and activate actuators with gpios
	return

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

receive()

