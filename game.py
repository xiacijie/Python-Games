import pygame,sys,time
import random
#RBG color setting
black = (0,0,0)
white = (255,255,255)
blue = (0,255,255)

#size setting 
screen_size = 800
seg_size = 15
speed = 0.36
FPS =15
#initialize screen
screen = pygame.display.set_mode((screen_size,screen_size))

clock= pygame.time.Clock()

def main():
	
	pygame.init()
	game = Game()
	game.play()
		
		
class Game:
	def __init__(self):
	
		self.snake = Snake()
		self.game_play = True
		
	def play(self):
		global clock
		while self.game_play:
			
			
			clock.tick(FPS)
			self.snake.draw_snake()
			self.get_key()
			self.snake.snake_move()
			if self.snake.if_snake_dies():
				self.game_play = False

			pygame.display.flip()
			pygame.display.update()
			screen.fill(black)	
			

			
			
			
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


	
class Segment:
	def __init__(self,left,top):
		global seg_size,speed,FPS
		self.top = top
		self.left = left
		self.direction = "up"
		self.x_speed = 0
		self.y_speed = speed*FPS
		self.rect = pygame.Rect(left,top,seg_size,seg_size)
		self.prev = None
		

class Snake:
	def __init__(self):

		global screen_size,seg_size
		self.snack_stack = []
		

		top = ((screen_size//seg_size)//2)*seg_size
		left = top
		self.head = Segment(top,left)


		self.snack_stack.append(self.head)
		self.body1= Segment(self.head.rect.left,self.head.rect.top+seg_size)
		
		self.body1.prev = self.head

		self.body2 = Segment(self.body1.rect.left,self.body1.rect.top+seg_size)
	
		self.body2.prev = self.body1

		self.snack_stack.append(self.body1)
		self.snack_stack.append(self.body2)
		self.order = 0

	def draw_snake(self):
		global screen,white
		for seg in self.snack_stack:
			r = random.randint(0,255)
			b = random.randint(0,255)
			g = random.randint(0,255)
			pygame.draw.rect(screen,(r,b,g),seg.rect,5)

	
	def snake_move(self): 
		
		for seg in self.snack_stack:
			self.seg_move(seg)

		
			
		
	def if_snake_dies(self):
		global screen_size
		if self.snack_stack[0].rect.top == 0:
			return True
		elif self.snack_stack[0].rect.right == screen_size:
			return True

		elif self.snack_stack[0].rect.left == 0:
			return True
		elif self.snack_stack[0].rect.bottom == screen_size:
			return True

	def set_speed(self,seg):

		global FPS,speed

		inner_speed = FPS*speed
		if seg.direction == "up":
			x_speed = 0
			y_speed = -inner_speed
		elif seg.direction == "down":
			x_speed = 0
			y_speed = inner_speed
		elif seg.direction == "left":
			x_speed = -inner_speed
			y_speed = 0
		elif seg.direction == "right":
			x_speed = inner_speed
			y_speed = 0
		seg.x_speed = x_speed
		seg.y_speed = y_speed

	def change_direction(self,direction):
		self.snack_stack[0].direction = direction
		





main()