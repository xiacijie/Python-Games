import pygame,sys,random
import sqlite3
import time
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
		self.border = Border()
		self.central = Central_line()
		self.your_car = Your_car() 
		
		self.enemy_car_list = []

		self.start_time = time.time()

	def draw_objects(self):
		self.border.draw()
		self.central.draw()
		self.your_car.draw()
		self.draw_enemy_cars()

	def create_enemy_cars(self):
		
		if len(self.enemy_car_list) < 2:
			self.enemy_car_list.append(Enemy_car())

	def draw_enemy_cars(self):
		for car in self.enemy_car_list:
			car.draw()

	def move_enemy_cars(self):
		for car in self.enemy_car_list:
			car.move()

	def delete_enemy_cars(self):
		for car in self.enemy_car_list:
			if car.rect.top >screen_size:
				self.enemy_car_list.remove(car)

	def play(self):
		while True:
			clock.tick(FPS)
			self.draw_objects()
			self.update_objects()
			self.get_key()
			pygame.display.update()
			screen.fill(black)

	def update_objects(self):
		self.move_enemy_cars()
		self.create_enemy_cars()
		self.delete_enemy_cars()


	def get_key(self): #Get the user input through the key board

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP: 
					self.your_car.move("up")
				elif event.key == pygame.K_DOWN:
					self.your_car.move("down")			
				elif event.key == pygame.K_LEFT:
					self.your_car.move("left")
				elif event.key == pygame.K_RIGHT:
					self.your_car.move("right")

class Segment:
	def __init__(self,left,top,width,height):
		self.rect = pygame.Rect(left,top,width,height)

class Border:

	def __init__(self):
		self.left_border = []
		self.right_border = []
		self.create_border()

	def create_border(self):
		height = 40
		top = 0
		width = 10
		# create left border
		for i in range(screen_size//(height)):
			segment = Segment(screen_size//4,top,width,height)
			self.left_border.append(segment)
			top += height
			

		#create right border
		top = 0
		for i in range(screen_size//(height)):
			segment = Segment(3*(screen_size//4),top,width,height)
			self.right_border.append(segment)
			top += height
		
	def draw(self):
		for i in range(len(self.left_border)):
			seg = self.left_border[i]
			#if i %2 == 0:
			pygame.draw.rect(screen,white,seg.rect,0)
			#else:
				#pygame.draw.rect(screen,black,seg.rect,0)

		for i in range(len(self.right_border)):
			seg = self.right_border[i]
			#if i %2 == 0:
			pygame.draw.rect(screen,white,seg.rect,0)
			#else:
				#pygame.draw.rect(screen,black,seg.rect,0)




class Central_line:
	def __init__(self):

		self.left_central = []
		self.right_central = []
		self.create_central()

	def create_central(self):

		height = 40
		top = 0
		width = 3

		# create left central
		for i in range(screen_size//(height)):
			segment = Segment((screen_size//4)+(screen_size//2//3),top,width,height)
			self.left_central.append(segment)
			top += height
			

		#create right border
		top = 0
		for i in range(screen_size//(height)):
			segment = Segment((screen_size//4)+(2*(screen_size//2//3)),top,width,height)
			self.right_central.append(segment)
			top += height

	def draw(self):
		for i in range(len(self.left_central)):
			seg = self.left_central[i]
			if i %2 == 0:
				pygame.draw.rect(screen,white,seg.rect,0)
			else:
				pygame.draw.rect(screen,black,seg.rect,0)

		for i in range(len(self.right_central)):
			seg = self.right_central[i]
			if i %2 == 0:
				pygame.draw.rect(screen,white,seg.rect,0)
			else:
				pygame.draw.rect(screen,black,seg.rect,0)




class Your_car:
	def __init__(self):
		car_size = 60
		left = screen_size//2 - car_size//2
		top = screen_size - car_size
		self.rect = pygame.Rect(left,top,car_size,car_size)
		self.speed = 3


	def draw(self):
		pygame.draw.rect(screen,blue,self.rect,0)

	def move(self,direction): #TO BE COMPLETED: CONSTRAINT THE MOVING RANGE!!!
		x_speed = 0
		y_speed = 0
		if direction == "up":
			y_speed = -self.speed

		elif direction == "down":
			y_speed = self.speed

		elif direction == "left":
			x_speed = -self.speed

		elif direction == "right":
			x_speed = self.speed

		self.rect.move_ip(x_speed,y_speed)


class Enemy_car: # TO be completed, randomly generate cars

	def __init__(self):
		car_size = 60
		pos1 = screen_size//2 - car_size//2
		pos2 = screen_size//4 + screen_size//12 -car_size//2
		pos3 = screen_size//4 + 5*(screen_size//12) - car_size//2
		left_pos = [pos1,pos2,pos3]
		pos = random.choice(left_pos)

		
		top = 0
		self.rect = pygame.Rect(pos,top,car_size,car_size)
		self.speed = 2

	def draw(self):
		pygame.draw.rect(screen,blue,self.rect,0)

	def move(self):
		self.rect.move_ip(0,self.speed)



main()