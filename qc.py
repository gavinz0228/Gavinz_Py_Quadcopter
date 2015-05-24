from RPIO import PWM
from mpu import *
import serial
import RPi.GPIO as GPIO
import time
import math
import datetime
#GPIO.setmode(GPIO.BCM)
leftPin=17
rightPin=18
upPin=22
max=2000
min=1000
servo=PWM.Servo()
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
baseSpeed=1000
lastTime=None
pidX=0
pidY=0
angleX=0
lastAngleX=0
lastAngleY=0
angleY=0
kpX=5
kiX=5
kdX=5
kpY=10
kiY=10
kdY=10
msg=0
# Read message from the serial port
ser=serial.Serial("/dev/ttyAMA0",timeout=0)
def run():
	global baseSpeed
	init()
	while True:		
		try:
			if ser.inWaiting():
				msg=ser.read(ser.inWaiting())
				if(msg=='u'):
					baseSpeed+=20
				elif(msg=='d'):
					baseSpeed-=20
				print(msg)			
				print(baseSpeed)
		except Exception as e:
			print(e)
		pidX,pidY=calculate(0,0)
		print("PID-Y:"+str(pidY))
		print("Base Power:"+str(baseSpeed))
		#ySpeed=getTransY()*10
		setSpeed(leftPin,baseSpeed-transform(pidY))
		setSpeed(upPin,baseSpeed+transform(pidX))
		setSpeed(rightPin,baseSpeed+transform(pidY))
		time.sleep(0.05)
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
	pidX=kpX*(goalX-angleX)+kiX*(lastAngleX-angleX)*interval+kdX*(lastAngleX-angleX)/interval
	lastAngleX=angleX
	lastAngleY=angleY
	lastTime=time.time()
	return pidX,pidY
def transform(value):
	return value/math.cos(math.radians(45))
def init():
	setSpeed(leftPin,min)
	setSpeed(rightPin,min)
	setSpeed(upPin,min)
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
