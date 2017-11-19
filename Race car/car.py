import pygame,sys,random
import sqlite3
pygame.init()
pygame.font.init()


#RBG color setting
black = (0,0,0)
white = (255,255,255)
deep_blue = (25,25,112)
blue = (0,0,255)
shalow_blue = (0,153,255)
green = (0,100,0)
bright_green = (0,255,0)
red = (255,0,0)
grey = (205,201,201)
dark_grey = (102,102,153)
yellow = (255,255,0)
purple = (160,32,240)
#size setting 
screen_size = 600
seg_size = 15
speed = 0.36
brick_width = 50
brick_height = 20
FPS = 60
#initialize screen
screen = pygame.display.set_mode((screen_size,screen_size))
pygame.key.set_repeat(10,5)
clock = pygame.time.Clock()
#back_groung_pic = pygame.image.load("back.jpg")
#pygame.mixer.music.load("back.mp3")
#Connection to the database
connection = None
cursor = None

def main():
	game = Game()
	game.play()


class Game:

	def __init__(self):
		pass

	def play(self):
		while True:
			self.get_key()

	def get_key(self): #Get the user input through the key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

class Border:
	def __init__(self):
		pass


class Your_car:
	def __init__(self):
		self.rect = pygame.Rect()

main()