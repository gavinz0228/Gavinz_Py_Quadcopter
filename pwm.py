from RPIO import PWM
import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BCM)
pin=22
max=2000
min=1000
servo=PWM.Servo()
def calibrate():
	
	servo.set_servo(pin,max)
	key=raw_input("waiting")
	print(key)
	servo.set_servo(pin,min)
	#time.sleep(2)
	key=raw_input("waiting")
	
def run():
	servo.set_servo(pin,min)
	time.sleep(2)
	while True:
		servo.set_servo(pin,1500)
		print('yay')
		time.sleep(1)
if __name__=="__main__":
	calibrate()
	#run()
