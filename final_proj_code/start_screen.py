# !/usr/bin/python
#  -*- coding: utf-8 -*-
#import for pitftscreen
import pygame,pigame
from pygame.locals import *
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math

#import for sound localization
import numpy as np
import wave
import struct

#import for email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#import for camera
from picamera2 import Picamera2, Preview
from datetime import datetime

#PiTFT
from pitft_touchscreen import pitft_touchscreen
from time import sleep

start_time = time.time()
quit = False

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

#Images
camera_img = pygame.image.load("/home/pi/final_proj/camera.png")
scaled_camera = pygame.transform.scale(camera_img, (camera_img.get_width() // 16, camera_img.get_height() // 16))
camera_rect = scaled_camera.get_rect()
camera_rect.center = (160, 100)

#gpio setup for servo pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
servo_pwm = GPIO.PWM(27, 50)
servo = GPIO.PWM(17, 50)

#PiTFT
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False) #keeps mouse off of the pitft screen
pitft = pigame.PiTft()
lcd = pygame.display.set_mode((320, 240))
lcd.fill(BLACK)
pygame.display.update()

font = pygame.font.Font(None, 30)

def disp_text(text: str, x, y, color=WHITE):
	text_coords = {text:(x, y)}
	for k,v in text_coords.items():
		text_surface = font.render('%s'%k, True, color)
		rect = text_surface.get_rect(center=v)
		lcd.blit(text_surface, rect)

def send_email(sender_email, sender_password, receiver_email, subject, body, image_path):
	#MIME setup
	message = MIMEMultipart()
	message['From'] = sender_email
	message['To'] = receiver_email
	message['Subject'] = subject

	#attach body of message
	message.attach(MIMEText(body, 'plain'))

	#attach image to file
	with open(image_path, 'rb') as file:
		img = MIMEImage(file.read())
		message.attach(img)

	#send email via SMTP server
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
		server.login(sender_email, sender_password)
		server.sendmail(sender_email, receiver_email, message.as_string())

def email_main(receiver_email, selected_index):
	sender_email = "ece5725selfiecam@gmail.com"
	sender_password = "outryozkdudjoiaq"
	subject = "Here's your selfie!"
	message = "You look great ;)"
	image_path = f"/home/pi/final_proj/photo_library/selfie{selected_index}.jpg"
	#sending email
	send_email(sender_email, sender_password, receiver_email, subject, message, image_path)

def move_to_the_left():
	print ("turning left")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(3)
	servo.ChangeDutyCycle(8)
	sleep(2)
	picam2.capture_file(f"/home/pi/final_proj/photo_library/selfie{pic_index}.jpg")
	sleep(0.5)
	servo.ChangeDutyCycle(5)
	servo_pwm.ChangeDutyCycle(5)

def move_to_the_right():
	print ("turning right")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(8)
	servo.ChangeDutyCycle(8)
	sleep(2)
	picam2.capture_file(f"/home/pi/final_proj/photo_library/selfie{pic_index}.jpg")
	sleep(0.5)
	servo.ChangeDutyCycle(5)
	servo_pwm.ChangeDutyCycle(5)

def get_max_audio(index):
	print("starting max audio")
	audio_file = wave.open('outputfile.wav', 'r')
	print("loaded outputfile")
	if index:
		audio_file = wave.open('outputfile1.wav', 'r')
		print("loaded outputfile1")
	num_frames = audio_file.getnframes()
	print("num frames")
	framerate = audio_file.getframerate()
	print("framerate")
	audio_data = audio_file.readframes(num_frames)
	print("audio data loading")
	audio_data = np.frombuffer(audio_data, dtype=np.int16)
	print("audio data loaded")
	try:
		max = np.argmax((audio_data))
		print(f"max index found: " + str(max))
		return audio_data[max]
	except Exception as e:
		print("exception")
		return 0

#init camera
picam2 = Picamera2()
cam_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(cam_config)
picam2.start()

#library controls
library_index = 0
selected_index = 0
curr_image = scaled_camera
scaled_curr_image = curr_image
curr_image_rect = scaled_curr_image.get_rect()
curr_image_rect.center = (160, 100)

#camera controls
#cam_button_center = (290, 30)
#cam_button_radius = 25
pic_index = 0

#init start and quit buttons
lcd.blit(scaled_camera, camera_rect)
disp_text("Auto Selfie Camera", 160, 20)
disp_text('quit', 295, 220)
disp_text('start', 27, 220)
start = False
email = False
camera = False
library = False

#email input box setup
input_box = pygame.Rect(50, 100, 220, 40)
active = False
text = ''
email_font = pygame.font.Font(None, 24)
color = COLOR_INACTIVE

pygame.display.update()
try:
	#while time.time() - start_time < 60 and not quit:
	while not quit:
		#PiTFT
		pitft.update()
		# setup screen
		if start and not email and not camera and not library:
			lcd.fill(BLACK)
			disp_text('instructions:', 160, 20)
			disp_text('1. take some photos!', 160, 60, RED)
			disp_text('2. select your favorite', 160, 100, YELLOW)
			disp_text('3. enter your email', 160, 140, GREEN)
			disp_text('4. remember to smile :)', 160, 180, (0,0,255))
			disp_text('library', 35, 220)
			disp_text('email', 115, 220)
			disp_text('camera', 200, 220)
			disp_text('back', 290, 220)
			pygame.display.update()
		# email screen
		if start and email:
			print("email started")
			lcd.fill(BLACK)
			disp_text("enter email addr:", 160, 50)
			disp_text("back", 290, 220)
			txt_surface = email_font.render(text, True, color)
			print("visuals created")

			width = 220
			print("width of box calculated")
			input_box.w = width
			print("input box updated")

			lcd.blit(txt_surface, (input_box.x+5, input_box.y+5))
			print("blit")
			pygame.draw.rect(lcd, color, input_box, 2)
			print("rect")

			pygame.display.flip()
			print("email finished")
		# camera screen
		if start and camera:
			print("camera active")
			max = get_max_audio(0)
			max1 = get_max_audio(1)
			print("maxes calculated")
			if (max > 20000) or (max1 > 20000):
				print("handclap detected")
				difference = max - max1
				print ("difference" + str(difference))
				if difference < 250:
					print("moving left")
					move_to_the_left()
					print("photo taken")
					pic_index += 1
					print ("picindex updated")
				elif difference > 250:
					print("moving right")
					move_to_the_right()
					print("photo taken")
					pic_index += 1
					print("picindex updated")
				else:
					print("straight ahead")
					picam2.capture_file(f"/home/pi/final_proj/photo_library/selfie{pic_index}.jpg")
					print("photo taken")
					pic_index += 1
					print("picindex updated")
			else:
				print ("no handclap detected")
				sleep(1)
			print("end of camera")
		# event handler
		for event in pygame.event.get():
			# keyboard events for email entry
			if event.type == pygame.KEYDOWN:
				if active and email:
					if event.key == pygame.K_RETURN:
						print(f"Email entered: {text}")
						email_main(text, selected_index)
						text = ''
						lcd.fill(BLACK)
						disp_text("photo on the way!", 160, 50)
						pygame.display.update()
						active = False
						email = False
					elif event.key == pygame.K_BACKSPACE:
						text = text[:-1]
					else:
						text += event.unicode
			# mouse events for touchscreen
			if(event.type is MOUSEBUTTONDOWN):
				x,y = pygame.mouse.get_pos()
				if not start:
					lcd.fill(BLACK)
					print(x,y)
					#touch_loc_text = 'Touch at ' + str(x) + ', ' + str(y)
					#disp_text(touch_loc_text, 160, 120)
					lcd.blit(scaled_camera, camera_rect)
					disp_text('quit', 295, 220)
					disp_text('start', 27, 220)
					pygame.display.update()

					if y > 200:
						if x > 270:
							print("quitting...")
							pygame.quit()
							quit = True
						if  x < 50:
							print("starting...")
							start = True
					else:
						pass
				elif email:
					if input_box.collidepoint(event.pos):
						active = not active
					else:
						active = False
					color = COLOR_ACTIVE if active else COLOR_INACTIVE

					if y > 200:
						if x > 270:
							email = False
							active = False
				elif camera:
					#distance = math.sqrt((x - cam_button_center[0]) ** 2 + (y - cam_button_center[1]) ** 2)
					#if distance < cam_button_radius:
					#	print("camera button pressed")
					#	pic_index += 1
					if y > 200:
						if x > 270:
							camera = False
				elif library:
					if pic_index > 0:
						if x < 106:
							print("pressed prev")
							if library_index == 0:
								library_index = pic_index - 1
							else:
								library_index -= 1
							print("prev" + str(library_index))
							curr_image = pygame.image.load(f"/home/pi/final_proj/photo_library/selfie{library_index}.jpg")
							scaled_curr_image = pygame.transform.scale(curr_image, (curr_image.get_width() // 6, curr_image.get_height() // 6))
							curr_image_rect = scaled_curr_image.get_rect()
							curr_image_rect.center = (160, 90)
							lcd.blit(scaled_curr_image, curr_image_rect)
							pygame.display.update()
						if x > 106 and x < 213:
							print("pressed select")
							selected_index = library_index
							print("select" + str(selected_index))
							library = False
						if x > 213:
							print("pressed next")
							if library_index == (pic_index - 1):
								library_index = 0
							else:
								library_index += 1
							print("next" + str(library_index))
							curr_image = pygame.image.load(f"/home/pi/final_proj/photo_library/selfie{library_index}.jpg")
							scaled_curr_image = pygame.transform.scale(curr_image, (curr_image.get_width() // 6, curr_image.get_height() // 6))
							curr_image_rect = scaled_curr_image.get_rect()
							curr_image_rect.center = (160, 90)
							lcd.blit(scaled_curr_image, curr_image_rect)
							pygame.display.update()
					else:
						if x > 106 and x < 213:
							print("no photos in lib")
							library = False
				else:
					if y > 200:
						if x < 75:
							library = True
							lcd.fill(BLACK)
							if pic_index > 0:
								curr_image = pygame.image.load("/home/pi/final_proj/photo_library/selfie0.jpg")
								scaled_curr_image = pygame.transform.scale(curr_image, (curr_image.get_width() // 6, curr_image.get_height() // 6))
								curr_image_rect = scaled_curr_image.get_rect()
								curr_image_rect.center = (160, 90)
								lcd.blit(scaled_curr_image, curr_image_rect)
							else:
								lcd.blit(curr_image, curr_image_rect)
								print("else blit")
							disp_text("prev", 30, 220)
							disp_text("select", 160, 220)
							disp_text("next", 290, 220)
							pygame.display.update()
						elif x < 155 and x > 75:
							email = True
							lcd.fill(BLACK)
							disp_text("back", 290, 220)
							disp_text("enter email address:", 160, 50)

							input_box.w = 220
							pygame.draw.rect(lcd, color, input_box, 2)
							pygame.display.update()
						elif x < 270 and x > 155:
							camera = True
							lcd.fill(BLACK)
							#pygame.draw.circle(lcd, RED, cam_button_center, cam_button_radius)
							disp_text("say cheese :)", 160, 120, (0,0,255))
							disp_text("back", 290, 220)
							pygame.display.update()
						elif x > 270:
							start = False
							email = False
							camera = False
							library = False
							active = False
							lcd.fill(BLACK)
							lcd.blit(scaled_camera, camera_rect)
							disp_text("Auto Selfie Camera", 160, 20)
							disp_text('quit', 295, 220)
							disp_text('start', 27, 220)
							pygame.display.update()
					else:
						pass
except KeyboardInterrupt:
	pass
finally:
	#PiTFT
	del(pitft)
	GPIO.cleanup()
	servo_pwm.stop(0)
	servo.stop(0)
	picam2.stop()
	print("Done")
	import sys
	sys.exit(0)
 
