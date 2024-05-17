import pygame
import math
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

#size = width, height = 500, 300
size = width, height = 320, 240
speed1 =  [4,4]
speed2 = [2,2]
black = 0,0,0

screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("/home/pi/Downloads/ball.png")
scaled_ball1 = pygame.transform.scale(ball1, (ball1.get_width() // 8, ball1.get_height() // 8))
ballrect1 = scaled_ball1.get_rect()

ball2 = pygame.image.load("/home/pi/Downloads/tennis-ball.png")
scaled_ball2 = pygame.transform.scale(ball2, (ball2.get_width() // 16, ball2.get_height() // 16))
ballrect2 = scaled_ball2.get_rect()

def magnitude(vector):
	return math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))

def normalize(vector):
	magnitude_v = magnitude(vector)
	vector[1] = vector[1] / magnitude_v
	vector[0] = vector[0] / magnitude_v
	return vector

def v_add(vector1, vector2):
	return [vector1[0] + vector2[0], vector1[1] + vector2[1]]

def v_sub(vector1, vector2):
	return [vector1[0] - vector2[0], vector1[1] - vector2[1]]

def dot(vector1, vector2):
	return (vector1[0] * vector2[0]) + (vector1[1] * vector2[1])

def scale(vector, scalar):
	return [vector[0] * scalar, vector[1] * scalar] 

ballrect1 = ballrect1.move([100, 100])
FPS = 24
clock = pygame.time.Clock()

while time.time() - start_time < 30 and not quit:
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
		#normal_vector = normalize([speed1[0] - speed2[0], speed1[1] - speed2[0]])
		#normal_s1 = dot(speed1, normal_vector)
		#normal_s2 = dot(speed2, normal_vector)
		#speed1 = v_sub(speed1, scale(normal_vector, normal_s1))
		#speed1 = v_add(speed2, scale(normal_vector, normal_s2))
		#speed2 = v_sub(speed2, scale(normal_vector, normal_s2))
		#speed2 = v_add(speed1, scale(normal_vector, normal_s1))
		s1_0 = speed1[0]
		s1_1 = speed1[1]
		speed1[0] = speed2[0]
		speed1[1] = speed2[1]
		speed2[0] = s1_0
		speed2[1] = s1_1

	if (not GPIO.input(22)):
		quit = True
		print("quitting...")

	screen.fill(black)
	screen.blit(scaled_ball1, ballrect1)
	screen.blit(scaled_ball2, ballrect2)
	pygame.display.flip()
GPIO.cleanup()
print("Done")
