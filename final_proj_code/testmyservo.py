import RPi.GPIO as GPIO
import os
from time import sleep
from picamera2 import Picamera2, Preview
from datetime import datetime
import time
from time import sleep



GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)



def take_picture():
	picam2 = Picamera2()
	camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores = {"size": (640, 480)}, display = "lores")
	picam2.configure(camera_config)
	picam2.start_preview(Preview.QTGL)
	picam2.start()
	time.sleep(2)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	picam2.capture_file(f"your_selfie{timestamp}.jpg")
	sleep(3)
	picam2.stop_preview()

servo_pwm = GPIO.PWM(27, 50)
servo = GPIO.PWM(17, 50)
servo_pwm.start(0)
servo.start(0)
print ("turning left")
servo_pwm.ChangeDutyCycle(3)
sleep(1)
servo.ChangeDutyCycle(7.5)
sleep(2)
#servo_pwm.stop()
#servo.stop()
take_picture()
sleep(2)
#servo.start()
#servo_pwm.start()
sleep(1)
servo.ChangeDutyCycle(5)
sleep(1)
servo_pwm.ChangeDutyCycle(5)
sleep(1)

print ("turning right")
servo_pwm.ChangeDutyCycle(10)
sleep(1)
servo.ChangeDutyCycle(7.5)
sleep(5)
servo.ChangeDutyCycle(5)
sleep(1)
servo_pwm.ChangeDutyCycle(5)
sleep(1)


servo_pwm.stop(0)
servo.stop(0)
GPIO.cleanup()
