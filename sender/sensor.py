import RPi.GPIO as GPIO, time, os

GPIO.setmode(GPIO.BCM)

def RCtime(RCpin):
	reading = 0
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.output(RCpin, GPIO.LOW)
	time.sleep(0.05)

	GPIO.setup(RCpin, GPIO.IN)
	while(GPIO.input(RCpin) == GPIO.LOW):
		reading += 1
	return reading

while True:
	#GPIO.setup(24, GPIO.IN)
	#print (GPIO.input(24))
	try:
		print  RCtime(24)
	except KeyboardInterrupt:
		GPIO.cleanup();
		sys.exit()
