import RPi.GPIO as GPIO, time, os

GPIO.setmode(GPIO.BCM)

def RCtime(RCpin):
	reading = 0
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.output(RCpin, GPIO.LOW)
	time.sleep(0.1)

	GPIO.setup(RCpin, GPIO.IN)
	while(GPIO.input(RCpin) == GPIO.LOW):
		reading += 1
	return reading

while True:
	try:
            #print "Sensor 1: ", RCtime(24)
            #print "Sensor 2: ", RCtime(23)
            #print "Sensor 3: ", RCtime(25)
            #print "Sensor 4: ", RCtime(22)
            if (RCtime(24) < 30):
                print "1"
            if (RCtime(23) < 17):
                print "2"
            if (RCtime(25) < 30):
                print "3"
            if (RCtime(22) < 20):
                print "4"
	except KeyboardInterrupt:
		GPIO.cleanup();
		sys.exit()
