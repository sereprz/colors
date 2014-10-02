import pygame, sys, random, math
from pygame.locals import *

def hsv_to_rgb(h, s, v):
# see wikipedia for conversion
# https://en.wikipedia.org/wiki/HSL_and_HSV#Converting_to_RGB	
	c = v * s
	hhat = h/60
	x = c*(1-math.fabs(hhat % 2 - 1))
	
	r1, b1, g1 = 0, 0, 0
	
	if hhat >= 0 and hhat < 1:
		r1, b1, g1 = c, x, 0
	elif hhat >= 1 and hhat < 2:
		r1, b1, g1 = x, c, 0
	elif hhat >= 2 and hhat < 3:
		r1, b1, g1 = 0, c, x
	elif hhat >= 3 and hhat < 4:
		r1, b1, g1 = 0, x, c
	elif hhat >= 4 and hhat < 5:
		r1, b1, g1 = x, 0, c
	elif hhat >= 5 and hhat < 6:
		r1, b1, g1 = c, 0, x
		
	m = v - c
	return int(255*(r1+m)), int(255*(b1+m)), int(255*(g1+m))
	
pygame.init()

WHITE = (255, 255, 255)

DISPLAY = pygame.display.set_mode((300,250))
pygame.display.set_caption("Test")

DISPLAY.fill(WHITE)

h = random.randrange(1,360)

while True:
	DISPLAY.fill(WHITE)
	
	s1 = 0.5
	s2 = 0.25
	s3 = 0.70
	
	col1 = hsv_to_rgb(h, s1, 1)
	col2 = hsv_to_rgb(h, s2, 1)
	col3 = hsv_to_rgb(h, s3, 1)
	
	pygame.draw.rect(DISPLAY, col1 , (10,10,50, 50))
	pygame.draw.rect(DISPLAY, col2 , (60,10,50, 50))
	pygame.draw.rect(DISPLAY, col3 , (10,60,50, 50))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	pygame.display.update()





		
	