from RPIO import PWM
from mpu import *
import RPi.GPIO as GPIO
import time
import math
import datetime
#GPIO.setmode(GPIO.BCM)
leftPin=17
rightPin=22
max=2000
min=1000
servo=PWM.Servo()
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
baseSpeed=1300
lastTime=None
pidX=0
pidY=0
angleX=0
lastAngleX=0
lastAngleY=0
angleY=0
kpX=1
kiX=1
kdX=1
kpY=1.5
kiY=1.5
kdY=1.5
def run():
	init()
	while True:
		pidX,pidY=calculate(0,0)
		print("PID-Y:"+str(pidY))
		#ySpeed=getTransY()*10
		setSpeed(leftPin,baseSpeed-transform(pidY))
		#time.sleep(0.1)
		setSpeed(rightPin,baseSpeed+transform(pidY))
		time.sleep(0.02)
def calculate(goalX,goalY):
	global lastTime
	global angleX
	global angleY
	global lastAngleX
	global lastAngleY
	if not lastTime:
		lastTime=time.time()
		return 0,0
	interval=time.time()-lastTime
	gx,gy,gz=get_gyro_rate()
	acX,acY=get_acc()
	angleX=0.98*(angleX+gx*interval)+0.02*acX
	angleY=0.98*(angleY+gy*interval)+0.02*acY
	#angleY+=gy*(interval/1000.0)
	print("Angle Y:"+str(transform(angleY)))
	
	#pidX=kpX*(goalX-acX)+kiX*(lastX-acX)*interval+kdX*(lastX-acX)/interval
	#pidY=kpY*(goalY-acY)+kiY*(lastY-acY)*interval+kdY*(lastY-acY)/interval
	pidY=kpY*(goalY-angleY)+kiY*(lastAngleY-angleY)*interval+kdY*(lastAngleY-angleY)/interval
	lastAngleX=angleX
	lastAngleY=angleY
	lastTime=time.time()
	return pidX,pidY
def transform(value):
	return value/math.cos(math.radians(45))
def init():
	setSpeed(leftPin,min)
	setSpeed(rightPin,min)
	time.sleep(2)
def setSpeed(pin,speed):
	speed=int(speed)
	if speed>max:
		speed=max
	elif speed<min:
		speed=min
	speed=speed/10*10
	servo.set_servo(pin,int(speed))	
if __name__=="__main__":
	#calibrate()
	run()
