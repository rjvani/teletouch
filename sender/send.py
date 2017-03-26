import socket

UDP_IP = "172.20.10.21" #receiver's IP
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
	return test

def send():
	#constantly sending to receiver pi
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print "Sending..."
	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_Port
	print 'message:',MSG
	while (1):
		data = sense()
		dataToSend = str(data)
		sock.sendto(dataToSend, (UDP_IP, UDP_Port))

send()

