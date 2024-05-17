import pygame,pigame
from pygame.locals import *
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math

#import for email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from pitft_touchscreen import pitft_touchscreen

start_time = time.time()

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

def email_main(receiver_email):
	sender_email = "ece5725selfiecam@gmail.com"
	sender_password = "outryozkdudjoiaq"
	subject = "Automated Test"
	message = "Hey did this work??"
	image_path = "/home/pi/final_proj/test.jpg"

	#sending email
	send_email(sender_email, sender_password, receiver_email, subject, message, image_path)

#pitft
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

pygame.init()

pitft = pigame.PiTft()
screen = pygame.display.set_mode((320, 240))

#colors
BLACK = (0,0,0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
color = COLOR_INACTIVE

#input box setup
input_box = pygame.Rect(50, 100, 220, 40)
active = False
text = ''
font = pygame.font.Font(None, 24)

running = True
while running and time.time() - start_time < 30:
	pitft.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type is pygame.MOUSEBUTTONDOWN:
			if input_box.collidepoint(event.pos):
				active = not active
			else:
				active = False
			color = COLOR_ACTIVE if active else COLOR_INACTIVE
		if event.type == pygame.KEYDOWN:
			if active:
				if event.key == pygame.K_RETURN:
					print(f"Email entered: {text}")
					email_main(text)
					text = ''
				elif event.key == pygame.K_BACKSPACE:
					text = text[:-1]
				else:
					text += event.unicode

	screen.fill(BLACK)
	txt_surface = font.render(text, True, color)

	width = max(220, txt_surface.get_width()+10)
	input_box.w = width

	screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
	pygame.draw.rect(screen, color, input_box, 2)

	pygame.display.flip()

pygame.quit()
del(pitft)
import sys
sys.exit(0)
