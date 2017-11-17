import pygame,sys
pygame.init()
pygame.font.init()


#RBG color setting
black = (0,0,0)
white = (255,255,255)
deep_blue = (25,25,112)
blue = (0,0,255)
green = (0,100,0)
red = (255,0,0)
grey = (205,201,201)
yellow = (255,255,0)
purple = (160,32,240)
#size setting 
screen_size = 600
seg_size = 15
speed = 0.36
brick_width = 100
brick_height = 20
FPS = 60
#initialize screen
screen = pygame.display.set_mode((screen_size,screen_size))
pygame.key.set_repeat(10,5)
clock = pygame.time.Clock()
#back_groung_pic = pygame.image.load("grass.jpg")
#pygame.mixer.music.load("back1.mp3")
#Connection to the database
connection = None
cursor = None
def main():
	game = Game()
	game.play()

class Game:
	def __init__(self):
		self.ball = Ball()
		self.game_play  = True
		self.board = Board()
		self.brick_list = []

	def create_bricks(self):
		top = 0
		for i in range(5):
			left = 0
			for j in range(screen_size//brick_width):
				new_brick = Brick(left,top,white)
				self.brick_list.append(new_brick)
				left += brick_width
			top += brick_height

	def draw_bricks(self):
		for brick in self.brick_list:
			brick.draw()

	def play(self):
		self.create_bricks()

		while self.game_play:
			clock.tick(FPS)
			self.draw_bricks()
			self.ball.draw()
			self.ball.move()
			self.ball.bounce_edge()
			
			self.board.draw()
			self.get_key()
			if self.if_ball_hit_board():
				self.ball.bounce_board()

			if self.if_ball_hit_brick():
				self.ball.bounce_brick()

			if self.if_game_lose():
				self.game_play = False

			
			pygame.display.update()
			screen.fill(black)

	def get_key(self): #Get the user input through the key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT: 
					self.board.move("left")
					if self.if_ball_hit_board():
						self.ball.bounce_board("left")
				elif event.key == pygame.K_RIGHT:
					self.board.move("right")
					if self.if_ball_hit_board():
						self.ball.bounce_board("right")


	def if_ball_hit_board(self):
		if self.board.rect.collidepoint(self.ball.x_coord,self.ball.y_coord):
			return True

	def if_game_lose(self):
		if self.ball.y_coord > screen_size:
			return True

	def if_ball_hit_brick(self):
		for brick in self.brick_list:
			if brick.rect.collidepoint(self.ball.x_coord,self.ball.y_coord):
				self.brick_list.remove(brick)
				return True


class Brick: # single brick
	def __init__(self,left,top,color):
		#self.left = left
		#self.top = top
		self.color = color
		
		self.rect = pygame.Rect(left,top,brick_width,brick_height)

	def draw(self):
		pygame.draw.rect(screen,blue,self.rect,0) # draw bricks
		pygame.draw.rect(screen,deep_blue,self.rect,1) #draw the border



class Ball: # single ball
	def __init__(self):
		self.x_coord = 300
		self.y_coord = 550
		self.x_speed = 0
		self.y_speed = -5
		self.radius = 5

	def draw(self):
		pygame.draw.circle(screen,white,(self.x_coord,self.y_coord),self.radius,0)

	def move(self):
		self.x_coord += self.x_speed
		self.y_coord += self.y_speed

	def bounce_edge(self):
		if self.x_coord <= 0+self.radius or self.x_coord >= screen_size - self.radius:
			self.x_speed = -self.x_speed
		elif self.y_coord <= 0+self.radius:
			self.y_speed = -self.y_speed

	def bounce_board(self,direction = None): # give the ball an x speed when the board is moving
		
		if direction == None:
			self.y_speed = -self.y_speed
		elif direction == "left":
			self.x_speed = -3
			
		elif direction == "right":
			self.x_speed = 3

	def bounce_brick(self):
		self.y_speed = -self.y_speed
			

class Board:
	def __init__(self):
		self.width = 100
		self.left = screen_size/2-0.5*self.width
		self.top = 560
		self.rect = pygame.Rect(self.left,self.top,self.width,5)
		self.x_speed = 10
		self.y_speed = 0

	def draw(self):
		pygame.draw.rect(screen,white,self.rect,0)

	def move(self,direction): # constraint the moving range
		if direction == "left":
			if self.x_speed > self.rect.left:
				self.x_speed = self.rect.left
		
			
			self.rect.move_ip(-self.x_speed,self.y_speed)
			
		else:
			if self.x_speed > screen_size-(self.rect.left + self.width):
				self.x_speed = screen_size-(self.rect.left + self.width)
			
			self.rect.move_ip(self.x_speed,self.y_speed)

		self.x_speed = 10
			




main()