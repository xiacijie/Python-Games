import pygame


class Tool:
	def __init__(self):
		#RBG color setting
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.blue = (25,25,112)
		self.green = (0,100,0)
		self.red = (255,0,0)
		self.grey = (205,201,201)
		self.yellow = (255,255,0)
		self.purple = (160,32,240)
		#create the clock
		self.clock = pygame.time.Clock()

		#DB connection
		self.connection = None
		self.cursor = None

	def create_window(self,length,width):
		self.screen = pygame.display.set_mode((screen_size,screen_size))
		return self.screen

	def connect_to_database(db_path):
		self.connection = sqlite3.connect(db_path)
		self.cursor = connection.cursor()

	def draw_text(self,content,font_size,coords,color):
		myfont = pygame.font.SysFont(None,font_size)
		textsurface = myfont.render(content,1,color)
		self.screen.blit(textsurface,coords)
