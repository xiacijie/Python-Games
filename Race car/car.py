import sys
sys.path.append('../common')
from common import *

left_border_pos = screen_size//4
right_border_pos = (screen_size // 4) * 3
car_width = 50
car_height = 100

enemy_car_image = pygame.image.load("enemy_car.png")
enemy_car_image = pygame.transform.scale(enemy_car_image, (car_width, car_height))

your_car_image = pygame.image.load("your_car.png")
your_car_image = pygame.transform.scale(your_car_image,(car_width,car_height))

def main():
	game = Game()
	game.play()



class Game:

	def __init__(self):
		self.border = Border()
		self.central = Central_line()
		self.your_car = Your_car() 
		# how may enemy cars
		self.car_num = 2
		self.start_time = time.time()
		self.enemy_car_list = []
		self.game_play = True
		self.start_time = time.time()
		self.recent_update = False # for level
		self.level = 1


	def update_game_status(self):

		if (self.detect_collide()):
			self.game_play = False

		self.draw_objects()
		self.update_objects()
		self.update_level()
		self.get_key()

	# detect if your car collides with enemy's car => lose
	def detect_collide(self):
		for c in self.enemy_car_list:
			if self.your_car.rect.colliderect(c.rect):
				return True

	def draw_time(self):
		self.time = time.time() - self.start_time
		draw_text("Time: %ds"%(self.time),30,(30,30),white)

	def draw_level(self):
		draw_text("Level: %d"%(self.level),30,(screen_size-100,30),white)
	
	def update_level(self):
		
		if (int(self.time) != 0 and int(self.time) % 5  == 0 ):
			if (not self.recent_update):

				self.level += 1
				self.car_num += 1
				self.recent_update = True
		else:
			self.recent_update = False


	def draw_objects(self):
		self.draw_time()
		self.draw_level()
		self.border.draw()
		self.central.draw()
		self.your_car.draw()
		self.draw_enemy_cars()

	def create_enemy_cars(self):
		
		pos1 = screen_size//2 - car_width//2
		pos2 = screen_size//4 + screen_size//12 -car_width//2
		pos3 = screen_size//4 + 5*(screen_size//12) - car_width//2
		left_pos = [pos1,pos2,pos3]


		speed_list = [1,3,3,3,3,5,6,8]
		

		

		while len(self.enemy_car_list) < self.car_num:
			# detect no two cars have the same position
			while (True):
				pos = random.choice(left_pos)
				for car in self.enemy_car_list:
					if (pos == car.pos):
						continue
				break
			# detect not two cars have the same speed
			while (True):
				speed = random.choice(speed_list)
				for car in self.enemy_car_list:
					if (speed == car.speed):
						continue
				break
			
			
			self.enemy_car_list.append(Enemy_car(pos,speed))

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
		while self.game_play:
			clock.tick(FPS)
			self.update_game_status()
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
			segment = Segment(left_border_pos,top,width,height)
			self.left_border.append(segment)
			top += height
			

		#create right border
		top = 0
		for i in range(screen_size//(height)):
			segment = Segment(right_border_pos,top,width,height)
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
		
		left = screen_size//2 - car_width//2
		top = screen_size - car_height
		self.rect = pygame.Rect(left,top,car_width,car_height)
		self.speed = 3



	def draw(self):
		screen.blit(your_car_image,(self.rect))
		# pygame.Surface.blit(image, screen, (100,100))
		# pygame.draw.rect(screen,blue,self.rect,0)

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

	def __init__(self,pos,speed):
		

		
		top = 0
		self.pos = pos
		self.rect = pygame.Rect(pos,top,car_width,car_height)
		self.speed = speed

	def draw(self):
		screen.blit(enemy_car_image,self.rect)

	def move(self):
		self.rect.move_ip(0,self.speed)



main()