import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()

servo_min = 0
servo_max = 2048

pwm.set_pwm_freq(250)

while True:
    channel = 12
    pwm.set_pwm(channel, 0, servo_min)
    pwm.set_pwm(channel, 0, servo_max)
