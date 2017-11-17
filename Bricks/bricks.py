import pygame,sys,random
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
back_groung_pic = pygame.image.load("back.jpg")
pygame.mixer.music.load("back.mp3")
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

class Game:
	def __init__(self):
		self.ball = Ball()
		self.game_play  = True
		self.board = Board()
		self.brick_list = []
		self.score = 0
		self.level = 1

	def create_bricks(self):
		top = 50
		for i in range(6):
			left = brick_width
			for j in range((screen_size-2*brick_width)//brick_width):
				r = random.randint(0,255)
				b = random.randint(0,255)
				g = random.randint(0,255)
				color = (r,b,g)
				new_brick = Brick(left,top,color)
				self.brick_list.append(new_brick)
				left += brick_width
			top += brick_height

	def show_score(self):
		font_size = 40
		coords = (10,10)
		draw_text("Score:%d"%self.score,font_size,coords,grey)

	def show_level(self):
		font_size = 40
		coords = (250,10)
		draw_text("Level:%d"%self.level,font_size,coords,grey)


	def draw_bricks(self):
		for brick in self.brick_list:
			brick.draw()

	def play(self):
		self.create_bricks()
		pygame.mixer.music.play(0,0)
		while self.game_play:
			clock.tick(FPS)
			self.draw_bricks()
			self.ball.draw()
			self.ball.move()
			self.ball.bounce_edge()
			
			self.board.draw()
			self.show_score()
			self.show_level()
			self.get_key()
			if self.if_ball_hit_board():
				self.ball.bounce_board()

			if self.if_ball_hit_brick():
				self.ball.bounce_brick()

			if self.if_game_lose():
				if self.end_screen():
					main()
				self.game_play = False
			if self.if_win():
				self.restart_game()

			
			pygame.display.update()
			screen.blit(back_groung_pic,(0,0))

	def end_screen(self):
		
		#show_congrats = (self.score>prev_high_score)
		while 1:
			screen.blit(back_groung_pic,(0,0))
			#if show_congrats:
				#draw_text("New Highest Score Reached",40,(128,100),blue)
			    #draw_text("You Final Score:%d"%self.score,40,(170,200),blue)
			draw_text("Play Again Y/N",30,(230,300),grey)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_n:
						return False
						break
					else:
						return True
						break	

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
				self.score += 5
				return True

	def if_win(self):
		return len(self.brick_list) == 0

	def restart_game(self):
		self.create_bricks()
		self.level += 1
		self.ball.reset()

class Brick: # single brick
	def __init__(self,left,top,color):
		#self.left = left
		#self.top = top
		self.color = color
		
		self.rect = pygame.Rect(left,top,brick_width,brick_height) #board


	def draw(self):
		pygame.draw.rect(screen,self.color,self.rect,0) # draw bricks
		pygame.draw.rect(screen,black,self.rect,1) #draw the border



class Ball: # single ball
	def __init__(self):
		self.x_coord = 300
		self.y_coord = 550
		self.x_speed = 0
		self.y_speed = -5
		self.radius = 5

	def draw(self):
	
		pygame.draw.circle(screen,black,(self.x_coord,self.y_coord),self.radius,0)
		pygame.draw.circle(screen,yellow,(self.x_coord,self.y_coord),self.radius,1)

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

	def reset(self):
		self.x_coord = 300
		self.y_coord = 550
		self.x_speed = 0
		self.y_speed = -5

			

class Board:
	def __init__(self):
		self.width = 100
		self.left = screen_size/2-0.5*self.width
		self.top = 560
		self.rect = pygame.Rect(self.left,self.top,self.width,10)
		self.x_speed = 10
		self.y_speed = 0

	def draw(self):
		pygame.draw.rect(screen,grey,self.rect,0)
		pygame.draw.rect(screen,red,self.rect,3)
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