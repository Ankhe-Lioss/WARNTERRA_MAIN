from setting import *
import random

def load_menu(game):
	game.resume_img = pygame.image.load(os.path.join('images','menu','button_resume.png')).convert_alpha()
	game.options_img = pygame.image.load(os.path.join('images','menu','button_options.png')).convert_alpha()
	game.quit_img = pygame.image.load(os.path.join('images','menu','button_quit.png')).convert_alpha()
	game.video_img = pygame.image.load(os.path.join('images','menu','button_video.png')).convert_alpha()
	game.audio_img = pygame.image.load(os.path.join('images','menu','button_audio.png')).convert_alpha()
	game.keys_img = pygame.image.load(os.path.join('images','menu','button_keys.png')).convert_alpha()
	game.back_img = pygame.image.load(os.path.join('images','menu','button_back.png')).convert_alpha()
	game.start_img = pygame.image.load(os.path.join('images','menu','button_start.png')).convert_alpha()
	game.restart_img = pygame.image.load(os.path.join('images','menu','button_restart.png')).convert_alpha()
	game.startmenu_img = pygame.image.load(os.path.join('images','menu','button_startmenu.png')).convert_alpha()
	game.deathmenu_img = pygame.image.load(os.path.join('images','menu','death_menu.png')).convert_alpha()
	game.death_to_start_img = pygame.image.load(os.path.join('images','menu','button_death_to_start.png')).convert_alpha()
	game.death_to_quit_img = pygame.image.load(os.path.join('images','menu','button_death_to_quit.png')).convert_alpha()
	game.death_to_restart_img = pygame.image.load(os.path.join('images','menu','button_death_to_restart.png')).convert_alpha()
	game.bow_button_img = pygame.image.load(os.path.join('images','menu','button_bow.png')).convert_alpha()
	game.gauntlet_button_img=pygame.image.load(os.path.join('images','menu','button_gauntlet.png')).convert_alpha()
	game.title_img = pygame.image.load(os.path.join('images','menu','title.png')).convert_alpha()
	#load_audio
	game.start_menu_audio=pygame.mixer.Sound(os.path.join('audio','menu','Start_menu.wav'))
	game.start_menu_audio.set_volume(0.3)
	game.death_menu_audio=pygame.mixer.Sound(os.path.join('audio','menu','Death_menu.wav'))
	game.death_menu_audio.set_volume(0.04)
	#pause menu
	game.resume_button = Button(304, 125, game.resume_img, 1)
	game.quit_button = Button(304, 500, game.quit_img, 1)
	game.restart_button = Button(304, 250, game.restart_img, 1)
	game.startmenu_button = Button(304, 375, game.startmenu_img, 1)
	#option menu
	game.video_button = Button(226, 75, game.video_img, 1)
	game.audio_button = Button(225, 200, game.audio_img, 1)
	game.keys_button = Button(246, 325, game.keys_img, 1)
	game.back_button = Button(332, 450, game.back_img, 1)

	#start menu
	game.start_button = Button(535, 260, game.start_img, 1)
	game.quit_start_button = Button(510, 460, game.quit_img, 1)
	game.options_button = Button(510, 360, game.options_img, 1)

	#death menu
	game.death_to_quit_button = Button(400, 420, game.death_to_quit_img, 1)
	game.death_to_start_button = Button(400, 340, game.death_to_start_img, 1)
	game.death_to_restart_button = Button(400, 260, game.death_to_restart_img, 1)

	#weapon menu
	game.bow_button=Button(243, 249, game.bow_button_img, 0.5)
	game.gauntlet_button=Button(747, 197, game.gauntlet_button_img, 0.5)
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