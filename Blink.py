#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Make an led blinking.
# auther      : www.freenove.com
# modification: 2018/08/02
########################################################################
import RPi.GPIO as GPIO
import time



def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(18,GPIO.OUT)
	print ('using pin%d'%ledPin)

def loop():
	while True:
		print("LED on")
		GPIO.output(18,GPIO.HIGH)
		time.sleep(1)
		print ("LED off")
		GPIO.output(18,GPIO.LOW)
		time.sleep(1)

def destroy():
	GPIO.output(ledPin, GPIO.LOW)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

