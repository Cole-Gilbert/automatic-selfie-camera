import pygame
import os
import RPi.GPIO as GPIO
import time

start_time = time.time()
quit = False

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

size = width, height = 320, 240
speed1 =  [1,1]
speed2 = [2,2]
black = 0,0,0

screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("/home/pi/Downloads/ball.png")
scaled_ball1 = pygame.transform.scale(ball1, (ball1.get_width() // 2, ball1.get_height() // 2))
ballrect1 = scaled_ball1.get_rect()

ball2 = pygame.image.load("/home/pi/Downloads/tennis-ball.png")
scaled_ball2 = pygame.transform.scale(ball2, (ball2.get_width() // 8, ball2.get_height() // 8))
ballrect2 = scaled_ball2.get_rect()

while time.time() - start_time < 30 and not quit:
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
	if (not GPIO.input(22)):
		quit = True
		print("quitting...")

	screen.fill(black)
	screen.blit(scaled_ball1, ballrect1)
	screen.blit(scaled_ball2, ballrect2)
	pygame.display.flip()

GPIO.cleanup()
print("Done") 
