from setting import *
def load_menu(game):
	game.resume_img = pygame.image.load("images/menu/button_resume.png").convert_alpha()
	game.options_img = pygame.image.load("images/menu/button_options.png").convert_alpha()
	game.quit_img = pygame.image.load("images/menu/button_quit.png").convert_alpha()
	game.video_img = pygame.image.load('images/menu/button_video.png').convert_alpha()
	game.audio_img = pygame.image.load('images/menu/button_audio.png').convert_alpha()
	game.keys_img = pygame.image.load('images/menu/button_keys.png').convert_alpha()
	game.back_img = pygame.image.load('images/menu/button_back.png').convert_alpha()
	game.resume_button = Button(304, 125, game.resume_img, 1)
	game.options_button = Button(297, 250, game.options_img, 1)
	game.quit_button = Button(336, 375, game.quit_img, 1)
	game.video_button = Button(226, 75, game.video_img, 1)
	game.audio_button = Button(225, 200, game.audio_img, 1)
	game.keys_button = Button(246, 325, game.keys_img, 1)
	game.back_button = Button(332, 450, game.back_img, 1)
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action