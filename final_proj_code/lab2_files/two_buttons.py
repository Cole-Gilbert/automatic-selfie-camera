# !/usr/bin/python
#  -*- coding: utf-8 -*-
import pygame,pigame
from pygame.locals import *
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math

from pitft_touchscreen import pitft_touchscreen
from time import sleep

start_time = time.time()
quit = False

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False)
pitft = pigame.PiTft()
lcd = pygame.display.set_mode((320, 240))
lcd.fill(BLACK)
pygame.display.update()

font = pygame.font.Font(None, 30)

def disp_text(text: str, x, y):
	text_coords = {text:(x, y)}
	for k,v in text_coords.items():
		text_surface = font.render('%s'%k, True, WHITE)
		rect = text_surface.get_rect(center=v)
		lcd.blit(text_surface, rect)

#setup for ball collision
size = width, height = 320, 200
speed1 =  [4,4]
speed2 = [2,2]
black = 0,0,0

ball1 = pygame.image.load("/home/pi/Downloads/ball.png")
scaled_ball1 = pygame.transform.scale(ball1, (ball1.get_width() // 4, ball1.get_height() // 4))
ballrect1 = scaled_ball1.get_rect()

ball2 = pygame.image.load("/home/pi/Downloads/tennis-ball.png")
scaled_ball2 = pygame.transform.scale(ball2, (ball2.get_width() // 8, ball2.get_height() // 8))
ballrect2 = scaled_ball2.get_rect()

ballrect1 = ballrect1.move([100, 100])
FPS = 24
clock = pygame.time.Clock()

#init start and quit buttons
disp_text('quit', 300, 230)
disp_text('start', 22, 230)
start = False

pygame.display.update()
try:
#	collide_setup()
	while time.time() - start_time < 30 and not quit:
		pitft.update()
		# Scan touchscreen events
		if (not GPIO.input(22)):
			quit = True
			print("bailout")

		if start:
#			collide()
#			print ("started")
#			disp_text('quit', 300, 230)
#			disp_text('start', 22, 230)

			clock.tick(FPS)
			ballrect1 = ballrect1.move(speed1)
			ballrect2 = ballrect2.move(speed2)
			if ballrect1.left < 0 or ballrect1.right > width:
				speed1[0] = -speed1[0]
			if ballrect1.top < 0 or ballrect1.bottom > height:
				speed1[1] = -speed1[1]
			if ballrect2.left < 0 or ballrect2.right > width:
				speed2[0] = -speed2[0]
			if ballrect2.top < 0 or ballrect2.bottom > height:
				speed2[1] = -speed2[1]
			if ballrect2.colliderect(ballrect1):
				s1_0 = speed1[0]
				s1_1 = speed1[1]
				speed1[0] = speed2[0]
				speed1[1] = speed2[1]
				speed2[0] = s1_0
				speed2[1] = s1_1

			lcd.fill(black)
			disp_text('quit', 300, 230)
			disp_text('start', 22, 230)
			lcd.blit(scaled_ball1, ballrect1)
			lcd.blit(scaled_ball2, ballrect2)
			pygame.display.update()

#		print("leaves if statement for collide")
		for event in pygame.event.get():
#			print("in for loop for touch")
			if(event.type is MOUSEBUTTONDOWN):
				pass
			elif(event.type is MOUSEBUTTONUP):
#				print ("registered touch")
				x,y = pygame.mouse.get_pos()
				if not start:
#					print("touch coords")
					lcd.fill(BLACK)
					print(x,y)
					touch_loc_text = 'Touch at ' + str(x) + ', ' + str(y)
					disp_text(touch_loc_text, 160, 120)
					disp_text('quit', 300, 230)
					disp_text('start', 20, 230)
					pygame.display.update()

				if y > 200:
					if x > 270:
						print("quitting...")
						pygame.quit()
						quit = True
						import sys
						sys.exit(0)
					if  x < 50:
						print("starting...")
						start = True
				else:
					pass
#			sleep(1)
except KeyboardInterrupt:
	pass
finally:
	del(pitft)
	GPIO.cleanup()
	print("Done")
 
