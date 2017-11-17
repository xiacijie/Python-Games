import pygame,sys
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
FPS = 180
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


	def play(self):
		while self.game_play:
			clock.tick(FPS)
			self.ball.draw()
			self.ball.move()
			self.ball.bounce_edge()
			self.ball_bounce_board()
			self.board.draw()
			self.get_key()
			self.ball_bounce_board()
			self.board_is_moving = False
			pygame.display.update()
			screen.fill(black)

	def get_key(self): #Get the user input through the key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT: 
					self.board.move("left")
					#self.ball_bounce_board("left")
				elif event.key == pygame.K_RIGHT:
					self.board.move("right")
					#self.ball_bounce_board("right")


	def ball_bounce_board(self):
		if self.board.rect.collidepoint(self.ball.x_coord,self.ball.y_coord):
			self.ball.bounce_board()



class Brick: # single brick
	def __init__(self):
		pass

class Ball: # single ball
	def __init__(self):
		self.x_coord = 300
		self.y_coord = 550
		self.x_speed = 0
		self.y_speed = -1
		self.radius = 5

	def draw(self):
		pygame.draw.circle(screen,white,(self.x_coord,self.y_coord),self.radius,0)

	def move(self):
		self.x_coord += self.x_speed
		self.y_coord += self.y_speed

	def bounce_edge(self):
		if self.x_coord == 0+self.radius or self.x_coord == screen_size - self.radius:
			self.x_speed = -self.x_speed
		elif self.y_coord == 0+self.radius:
			self.y_speed = -self.y_speed

	def bounce_board(self):
		
		self.y_speed = -self.y_speed
		#if direction == "left":
			#self.x_speed = -10
		#elif direction == "right":
			#self.x_speed = 10

class Board:
	def __init__(self):
		width = 30
		left = screen_size/2-0.5*width
		self.rect = pygame.Rect(left,560,70,5)

	def draw(self):
		pygame.draw.rect(screen,white,self.rect,0)

	def move(self,direction):
		if direction == "left":
			self.rect.move_ip(-10,0)
		else:
			self.rect.move_ip(10,0)




main()