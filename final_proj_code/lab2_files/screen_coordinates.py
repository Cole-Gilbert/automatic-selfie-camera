# !/usr/bin/python
#  -*- coding: utf-8 -*-
import pygame,pigame
from pygame.locals import *
import os
import RPi.GPIO as GPIO
import time

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
lcd.fill((0,0,0))
pygame.display.update()

font = pygame.font.Font(None, 30)

def disp_text(text: str, x, y):
	text_coords = {text:(x, y)}
	for k,v in text_coords.items():
		text_surface = font.render('%s'%k, True, WHITE)
		rect = text_surface.get_rect(center=v)
		lcd.blit(text_surface, rect)

disp_text('quit', 300, 230)

pygame.display.update()
try:
	while time.time() - start_time < 30 and not quit:
		pitft.update()
		# Scan touchscreen events
		if (not GPIO.input(22)):
			quit = True
			print("quitting...")

		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONDOWN):
				pass
			elif(event.type is MOUSEBUTTONUP):
				lcd.fill(BLACK)
				x,y = pygame.mouse.get_pos()
				print(x,y)
				touch_loc_text = 'Touch at ' + str(x) + ', ' + str(y)
				disp_text(touch_loc_text, 160, 120)
				disp_text('quit', 300, 230)
				pygame.display.update()

				if y > 220:
					if x > 290:
						print("quitting...")
						pygame.quit()
						import sys
						sys.exit(0)
				else:
					pass
		sleep(1)
except KeyboardInterrupt:
	pass
finally:
	del(pitft)
	GPIO.cleanup()
	print("Done")
