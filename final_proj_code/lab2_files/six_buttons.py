import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
	time.sleep(0.2)
	if ( not GPIO.input(17) ):
		print("Button 17 has been pressed")
	elif ( not GPIO.input(22) ):
		print("Button 22 has been pressed")
	elif ( not GPIO.input(23) ):
		print("Button 23 has been pressed")
	elif ( not GPIO.input(27) ):
		print("Button 27 has been pressed")
	elif ( not GPIO.input(26) ):
		print("Button 26 has been pressed")
	elif ( not GPIO.input(16) ):
		print("Button 16 has been pressed")
