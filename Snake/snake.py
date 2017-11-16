import pygame,sys,time
import random,math
import sqlite3

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
back_groung_pic = pygame.image.load("grass.jpg")

#Connection to the database
connection = None
cursor = None


def main():
	global connection,cursor
	connection = sqlite3.connect("score.db")
	cursor = connection.cursor()
	game = Game()
	game.play()

# draw the string to the screen
def draw_text(content,font_size,coords,color):
	myfont = pygame.font.SysFont(None,font_size)
	textsurface = myfont.render(content,1,color)
	screen.blit(textsurface,coords)

#To be completed
def get_input():
	pass

class Game:
	def __init__(self):
	
		self.snake = Snake()
		self.game_play = True
		self.apple = Apple()
		self.start_time = time.time()
		self.level = 1
		self.score_add = 5
		self.stored_length = 0
		self.fps = FPS

	def show_score(self,coords,font_size):
		self.score = self.snake.length * self.score_add - 20
		draw_text("Score:%d"%self.score,font_size,coords,blue)

	def show_time(self,coords,font_size):
		self.time1 = time.time()-self.start_time
		draw_text("Time:%d"%self.time1,font_size,coords,blue)

	def show_level(self,coords,font_size):
		draw_text("Level:%d"%self.level,font_size,coords,blue)

	def get_highest_score(self):
		cursor.execute("select max(score) from score;")
		row = cursor.fetchone()
		if row[0] == None:
			highest_score = 0
		else:
			highest_score = row[0]
		return highest_score

	def show_highest_score(self,coords,font_size):
		draw_text("Highest Score:%d"%self.get_highest_score(),font_size,coords,blue)



	def draw_boundary(self):
		boundary = pygame.Rect(0,0,screen_size,screen_size)
		pygame.draw.rect(screen,black,boundary,15)

	#The key method, controlling the whole game 
	def play(self):
		
		self.apple.randomize()
		for i in range(0,3):
			self.snake.snake_grow()
		while self.game_play:
			
			clock.tick(FPS)
			self.show_highest_score((10,15),30)
			self.show_score((250,15),30)
			self.show_time((350,15),30)
			self.show_level((450,15),30)
			self.draw_boundary()
			self.apple.draw()
			self.snake.draw_snake()
			self.get_key()
			self.snake.snake_move()
			self.level_up()
			if self.if_snake_eat_apple():
				self.snake.snake_grow()
				self.apple.randomize()

			if self.snake.if_snake_dies():
				prev_high_score = self.get_highest_score()
				self.store_into_database()
				if self.end_screen(prev_high_score):
					main()
				
				self.game_play = False
				connection.close()


			pygame.display.flip()
			pygame.display.update()
			screen.blit(back_groung_pic,(0,0))	
			
	def get_key(self): #Get the user input through the key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP: 
					self.snake.change_direction("up")
				elif event.key == pygame.K_DOWN:
					self.snake.change_direction("down")				
				elif event.key == pygame.K_LEFT:
					self.snake.change_direction("left")
				elif event.key == pygame.K_RIGHT:
					self.snake.change_direction("right")
				

	def level_up(self):
		global FPS
		
		snake_length = self.snake.length
		up = False
		if snake_length == 8 or snake_length == 15 or snake_length == 25 or snake_length == 30 or snake_length == 40 or snake_length == 50 or snake_length == 60 or snake_length == 70:
			up = True
			

		if up and self.stored_length != snake_length:
			self.fps += 3
			self.level += 1
			self.score_add += 5
			draw_text("LEVEL UP",60,(220,300),yellow)
			pygame.display.update()
			time.sleep(1)
			self.stored_length = snake_length

	def end_screen(self,prev_high_score):
		
		show_congrats = (self.score>prev_high_score)
		while 1:
			screen.blit(back_groung_pic,(0,0))
			if show_congrats:
				draw_text("New Highest Score Reached",40,(128,100),blue)
			draw_text("You Final Score:%d"%self.score,40,(170,200),blue)
			draw_text("Play Again Y/N",30,(230,300),blue)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_n:
						return False
						break
					else:
						return True
						break

	def if_snake_eat_apple(self):
		if self.snake.head.rect.colliderect(self.apple.rect):
			return True

	def store_into_database(self):
		cursor.execute("select count(*) from score;")
		row = cursor.fetchone()

		if row == None:
			new_pid = 1
		else:
			new_pid = row[0] + 1
		data_record = (new_pid,self.score,self.level,self.time1)
		cursor.execute("insert into score values (?,?,?,?);",data_record)
		connection.commit()


	
class Segment:
	def __init__(self,left,top):
		
		self.rect = pygame.Rect(left,top,seg_size,seg_size)
		self.prev = None
		self.next = None
		self.direction = "up"

class Snake:
	def __init__(self):

		self.head = Segment(((screen_size//seg_size)//2)*seg_size, ((screen_size//seg_size)//2)*seg_size)
		self.length = 1
		self.head_direction = "up"
		self.x_speed = 0
		self.y_speed = -seg_size

	def draw_snake(self):

		current = self.head
		pygame.draw.rect(screen,yellow,current.rect,0)
		current =current.next
		while current!= None:
			pygame.draw.rect(screen,green,current.rect,0)
			current = current.next

	# To be modified, how to make the snake turn around
	def snake_move(self):

		prev = None

		tail = self.head
		while tail.next != None:
			tail = tail.next

		while tail.prev != None:
			tail.rect.move_ip(tail.prev.rect.left-tail.rect.left, tail.prev.rect.top-tail.rect.top)
			tail.direction = tail.prev.direction
			tail = tail.prev

		self.set_speed()
		self.head.rect.move_ip(self.x_speed,self.y_speed)

	def snake_grow(self):

		last = self.head
		while last.next != None:
			last = last.next

		if last.direction == "up":
			top = last.rect.top + seg_size
			left = last.rect.left
		elif last.direction == "down":
			top = last.rect.top -seg_size
			left = last.rect.left
		elif last.direction == "left":
			top = last.rect.top
			left = last.rect.left + seg_size
		else:
			top = last.rect.top
			left = last.rect.left - seg_size	
		new_seg = Segment(left,top)
		new_seg.prev = last
		last.next = new_seg
		self.length += 1


	def if_snake_dies(self):

		if self.head.rect.top == 0:
			return True
		elif self.head.rect.left >= screen_size- seg_size+10:
			return True

		elif self.head.rect.left == 0:
			return True
		elif self.head.rect.top >=screen_size - seg_size+10:
			return True

		current = self.head.next
		while current != None:
			if self.head.rect.colliderect(current.rect):
				return True
			current = current.next

	def set_speed(self):

	
		if self.head.direction == "up":
			x_speed = 0
			y_speed = -seg_size
		elif self.head.direction == "down":
			x_speed = 0
			y_speed = seg_size
		elif self.head.direction == "left":
			x_speed = -seg_size
			y_speed = 0
		elif self.head.direction == "right":
			x_speed = seg_size
			y_speed = 0
		self.x_speed = x_speed
		self.y_speed = y_speed

	def change_direction(self,direction):
		if direction == "up" and self.head_direction == "down":
			return
		elif direction == "down" and self.head_direction == "up":
			return 
		elif direction == "left" and self.head_direction == "right":
			return
		elif direction == "right" and self.head_direction == "left":
			return 

		self.head_direction = direction
		self.head.direction = direction

class Apple:

	def draw(self):
		pygame.draw.rect(screen,red,self.rect,15)
	def randomize(self):
		left = random.randint(15,screen_size-15)
		top = random.randint(35,screen_size-15)
		self.rect = pygame.Rect(left,top,10,10)
		
main()