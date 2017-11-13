import pygame,sys

def main():
	pygame.init()

	screen = pygame.display.set_mode((500,400))
	black = (0,0,0)
	screen.fill(black)
	rect = pygame.Rect(20,20,20,20)
	pygame.draw.rect(screen,(255,255,255),rect,1)
	pygame.display.update()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		

main()