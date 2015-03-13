import vw
import time
import pigpio
RX=2
BPS=4000
pi=pigpio.pi()
rx=vw.rx(pi,RX,BPS)
tx=vw.tx(pi,TX,BPS)
while True:
	while not rx.ready():
		time.sleep(1)
	print(rx.get())
