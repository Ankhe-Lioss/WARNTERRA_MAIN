from setting import *
import random
def load_menu(game):
	game.resume_img = pygame.image.load("images/menu/button_resume.png").convert_alpha()
	game.options_img = pygame.image.load("images/menu/button_options.png").convert_alpha()
	game.quit_img = pygame.image.load("images/menu/button_quit.png").convert_alpha()
	game.video_img = pygame.image.load('images/menu/button_video.png').convert_alpha()
	game.audio_img = pygame.image.load('images/menu/button_audio.png').convert_alpha()
	game.keys_img = pygame.image.load('images/menu/button_keys.png').convert_alpha()
	game.back_img = pygame.image.load('images/menu/button_back.png').convert_alpha()
	game.start_img = pygame.image.load('images/menu/button_start.png').convert_alpha()
	game.resume_button = Button(304, 125, game.resume_img, 1)
	game.options_button = Button(304, 250, game.options_img, 1)
	game.quit_button = Button(304, 375, game.quit_img, 1)
	game.video_button = Button(226, 75, game.video_img, 1)
	game.audio_button = Button(225, 200, game.audio_img, 1)
	game.keys_button = Button(246, 325, game.keys_img, 1)
	game.back_button = Button(332, 450, game.back_img, 1)
	game.start_button = Button(640, 360, game.start_img, 1)
	game.quit_start_button = Button(640, 460, game.quit_img, 1)
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
		pos = pygame.mouse.get_pos()

		# Default position
		draw_x = self.rect.x
		draw_y = self.rect.y

		# Check if mouse is over the button
		if self.rect.collidepoint(pos):
			# Add slight random offset for "vibration" effect
			draw_x += random.randint(-1, 1)
			draw_y += random.randint(-1, 1)

			# Handle click
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				self.clicked = True
				action = True

		# Reset click when mouse released
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# Draw with possible vibration offset
		surface.blit(self.image, (draw_x, draw_y))

		return action