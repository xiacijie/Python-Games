import pygame,sys

def main():
	pygame.init()
	screen_size = 800

	screen = pygame.display.set_mode((screen_size,screen_size))

	#RBG color setting
	black = (0,0,0)
	white = (255,255,255)
	blue = (0,255,255)
	screen.fill(black)

	#Split the screen into grids
	grid_size = 40;
	grid_row_and_col = screen_size//grid_size
	num_of_grids = grid_row_and_col*grid_row_and_col

	#Draw the grids 
	
	rect_top = 0
	for i in range(grid_row_and_col):
		rect_left = 0
		for j in range(grid_row_and_col):
			rect = pygame.Rect(rect_left,rect_top,grid_size,grid_size)
			pygame.draw.rect(screen,blue,rect,1)
			rect_left += grid_size
		rect_top+= grid_size
	pygame.display.update()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
class Game:
	def __init__(self):
		pass

	def play(self):
		pass

	def get_quit(self):
		pass


class Snake:
	def __init__(self):
		


main()