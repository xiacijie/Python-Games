import pygame,sys,time
import random,math

pygame.init()
pygame.font.init()


#RBG color setting
black = (0,0,0)
white = (255,255,255)
blue = (0,255,255)
green = (0,255,0)
red = (255,0,0)
grey = (205,201,201)
yellow = (255,255,0)
#size setting 
screen_size = 800
seg_size = 15
speed = 0.36
FPS =12
#initialize screen
screen = pygame.display.set_mode((screen_size,screen_size))

clock = pygame.time.Clock()


def draw_text(content,font_size,coords,color):
	myfont = pygame.font.SysFont("monospace",font_size)
	textsurface = myfont.render(content,1,color)
	screen.blit(textsurface,coords)

def main():
	screen.fill(black)
	draw_text("qwerwqerwqreqwrewq",50,(20,20),white)
	
	pygame.display.update()
main()