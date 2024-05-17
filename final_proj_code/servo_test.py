import RPi.GPIO as GPIO
import os
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

servo_pwm = GPIO.PWM(27, 50)
servo_pwm.start(0)
servo_pwm.ChangeDutyCycle(1)
sleep(1)
servo_pwm.ChangeDutyCycle(5)
sleep(1)
servo_pwm.ChangeDutyCycle(10)
sleep(1)
servo_pwm.stop(0)
GPIO.cleanup()
