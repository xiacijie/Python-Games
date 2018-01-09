import pygame
import os
import sys


pygame.init()
pygame.font.init()
#RBG color setting
black = (0,0,0)
white = (255,255,255)
blue = (25,25,112)
green = (0,100,0)
red = (255,0,0)
grey = (205,201,201)
yellow = (255,255,0)
purple = (160,32,240)
#size setting 
screen_size = 600
seg_size = 15
speed = 0.36
FPS = 10
#initialize screen
screen = pygame.display.set_mode((screen_size,screen_size))

clock = pygame.time.Clock()
def main():
	ui = Ui()
	ui.run()

#draw text on screen
def draw_text(content,font_size,coords,color):
	myfont = pygame.font.SysFont(None,font_size)
	textsurface = myfont.render(content,1,color)
	screen.blit(textsurface,coords)




class Ui:
	def __init__(self):
		self.first_button = pygame.Rect(30,30,100,100)
		self.ui_run = True



	#draw the button
	def draw_button(self):
		pygame.draw.rect(screen,white,self.first_button,0)

	#detect whether to end the screen
	def get_key(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

	def run(self):
		while self.ui_run:
			screen.fill(black)
			self.draw_button()
			self.get_key()
			
			pygame.display.update()




main()