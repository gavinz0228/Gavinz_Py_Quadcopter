from RPIO import PWM
from mpu import *
import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BCM)
pin=17
max=2000
min=1000
motor=PWM.Servo()
baseSpeed=1200
def run():
	init()
	while True:
		addSpeed=getX()*10
		speed=baseSpeed+addSpeed
		setSpeed(pin,speed)
		time.sleep(0.1)
def init():
	setSpeed(pin,min)
	time.sleep(2)
def setSpeed(pin,speed):
	speed=int(speed)
	if speed>max:
		speed=max
	elif speed<min:
		speed=min
	speed=speed/10*10
	motor.set_servo(pin,int(speed))	
if __name__=="__main__":
	#calibrate()
	run()
