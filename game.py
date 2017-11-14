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



def main():
	

	game = Game()
	game.play()

def draw_text(content,font_size,coords,color):
	myfont = pygame.font.SysFont('Comic Sans MS',1,white)
	textsurface = myfont.render(content,False,color)
	screen.blit(textsurface,coords)

class Game:
	def __init__(self):
	
		self.snake = Snake()
		self.game_play = True
		self.apple = Apple()

	def draw_boundary(self):
		boundary = pygame.Rect(0,0,screen_size,screen_size)
		pygame.draw.rect(screen,blue,boundary,15)

	def play(self):

		self.apple.randomize()
		for i in range(0,3):
			self.snake.snake_grow()
		while self.game_play:
			
			clock.tick(FPS)
			
			self.draw_boundary()
			self.apple.draw()
			self.snake.draw_snake()
			self.get_key()
			self.snake.snake_move()
			if self.if_snake_eat_apple():
				self.snake.snake_grow()
				self.apple.randomize()
			if self.snake.if_snake_dies():
				self.game_play = False
			
			pygame.display.flip()
			pygame.display.update()
			screen.fill(grey)	
			

			
			
			
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
				return 1

	def if_snake_eat_apple(self):
		if self.snake.head.rect.collidepoint(self.apple.x_coord,self.apple.y_coord):
			return True

class Board:
	def __init__(self):
		point = 0
	
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
		pygame.draw.rect(screen,yellow,current.rect,4)
		current =current.next
		while current!= None:
			pygame.draw.rect(screen,green,current.rect,3)
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
		pygame.draw.circle(screen,red,(self.x_coord,self.y_coord),5,0)
	def randomize(self):
		self.x_coord = random.randint(15,screen_size-15)
		self.y_coord = random.randint(15,screen_size-15)
		

		



main()