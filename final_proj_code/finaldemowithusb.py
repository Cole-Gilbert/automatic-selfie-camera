import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from datetime import datetime
import wave
import struct
import matplotlib.pyplot as  plt
import subprocess


#output_file= '/home/pi/final_pro/output.wav'
record_command = [
	'arecord', '--format=S16_LE', '--rate=16000', '--file-type=wav', '--duration=4','out.wav'
]

subprocess.run(record_command, check = True)


audio_file = wave.open('out.wav', 'r')
num_frames = audio_file.getnframes()
framerate = audio_file.getframerate()


audio_data = audio_file.readframes(num_frames)

audio_data = np.frombuffer(audio_data, dtype=np.int16)


fft_data = np.fft.fft(audio_data)


freq_bins = np.fft.fftfreq(len(fft_data), 1.0/framerate)


plt.plot(freq_bins, np.abs(fft_data))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')


peak_idx = np.argmax(np.abs(fft_data))
peak_freq = freq_bins[peak_idx]
peak_amp = np.abs(fft_data[peak_idx])


print('Fundamental frequency:', peak_freq, 'Hz')


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
servo_pwm = GPIO.PWM(27, 50)
servo = GPIO.PWM(17, 50)


def move_to_the_left():
	print ("turning left")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(3)
	sleep(1)
	servo.ChangeDutyCycle(7.5)
	sleep(1)
	servo.ChangeDutyCycle(8)
	sleep(2)
#	take_picture()
	sleep(2)
	servo.ChangeDutyCycle(5)
	sleep(1)
	servo_pwm.ChangeDutyCycle(5)
	sleep(1)




def move_to_the_right():
	print ("turning right")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(8)
	sleep(1)
	servo.ChangeDutyCycle(7.5)
	sleep(2)
	servo.ChangeDutyCycle(8.5)
	sleep(1)
#	take_picture()
	sleep(1)
	servo.ChangeDutyCycle(5)
	sleep(1)
	servo_pwm.ChangeDutyCycle(5)
	sleep(1)


def take_picture():
	picam2 = Picamera2()
	camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores = {"size": (640, 480)}, display = "lores")
	picam2.configure(camera_config)
	picam2.start_preview(Preview.QTGL)
	picam2.start()
	time.sleep(2)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	picam2.capture_file(f"your_selfie{timestamp}.jpg")
	sleep(2)
	picam2.stop_preview()
	picam2.close()



if 6.0<= abs(peak_freq) <= 10:
	move_to_the_left()
else:
	harmonics=[]
	for i in range (2, 10):
		harmonic_freq = i*peak_freq
		if 7.0<=abs(harmonic_freq) <= 10:
			move_to_the_left()
			break
#else:
#       print("No frequency detected")
plt.show()
