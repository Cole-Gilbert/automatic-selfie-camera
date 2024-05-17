import pygame
import os
import RPi.GPIO as GPIO
import time

start_time = time.time()
quit = False

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')
pygame.init()

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

size = width, height = 320, 240
speed =  [1,1]
black = 0,0,0

screen = pygame.display.set_mode(size)
ball = pygame.image.load("/home/pi/Downloads/ball.png")
scaled_ball = pygame.transform.scale(ball, (ball.get_width() // 2, ball.get_height() // 2))
ballrect = scaled_ball.get_rect()

while time.time() - start_time < 30 and not quit:
	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]
	if (not GPIO.input(22)):
		quit = True
		print("quitting...")
	
	screen.fill(black)
	screen.blit(scaled_ball, ballrect)
	pygame.display.flip()

GPIO.cleanup()
print("Done")

