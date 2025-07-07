from setting import *
from helper import Description, Delay
import random
#button with action to check if u click on it
class Button:
	def __init__(self, x, y, image, scale=1):
		width = image.get_width()
		height = image.get_height()
		#custom scaling if needed
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		#loading graphic
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()[0]
		# Default position
		draw_x = self.rect.x
		draw_y = self.rect.y

		# Check if mouse is over the button
		if self.rect.collidepoint(pos):
			# Add slight random offset for "vibration" effect
			draw_x += random.randint(-1,1)
			draw_y += random.randint(-1,1)

			# Handle click
			if mouse_pressed and not self.clicked:
				self.clicked = True
				action = True
			else:
				# If mouse leaves the button while still pressed, cancel the click
				self.clicked = False

		# Reset click when mouse released

		if not mouse_pressed:
			self.clicked = False

		# Draw with possible vibration offset
		surface.blit(self.image, (draw_x, draw_y))

		return action
#init the menu button for use in menu
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
	game.start_menu_audio.set_volume(0.9)
	game.death_menu_audio=pygame.mixer.Sound(os.path.join('audio','menu','Death_menu.wav'))
	game.death_menu_audio.set_volume(0.4)
	#pause menu
	game.resume_button = Button(304, 125, game.resume_img)
	game.quit_button = Button(304, 500, game.quit_img)
	game.restart_button = Button(304, 250, game.restart_img)
	game.startmenu_button = Button(304, 375, game.startmenu_img)
	#option menu
	game.video_button = Button(226, 75, game.video_img)
	game.audio_button = Button(225, 200, game.audio_img)
	game.keys_button = Button(246, 325, game.keys_img)
	game.back_button = Button(332, 450, game.back_img)

	#start menu
	game.start_button = Button(535, 260, game.start_img)
	game.quit_start_button = Button(510, 460, game.quit_img)
	game.options_button = Button(510, 360, game.options_img)

	#death menu
	game.death_to_quit_button = Button(400, 420, game.death_to_quit_img)
	game.death_to_start_button = Button(400, 340, game.death_to_start_img)
	game.death_to_restart_button = Button(400, 260, game.death_to_restart_img)

	#weapon menu
	game.bow_button=Button(83, 453, game.bow_button_img, 0.25)
	game.gauntlet_button=Button(869,414, game.gauntlet_button_img, 0.25)
 



class Instruction_rect:
    def __init__(self, game, rect, description: Description = Description("Ah ah ah yeh yeh sussy baka shiba seki ramen aioshima boot skibidi bidi dom dom yes yes")):
        self.rect = rect
        self.description = description
        self.dialog = game.dialog_layout
        self.waiting = False
        self.active = False
        self.game = game
        self.timer = None

    def update(self, surface: pygame.Surface):
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))
            surface.blit(overlay, self.rect.topleft)
            
            if not self.waiting:
                self.waiting = True
                self.timer = Delay(1000, lambda: setattr(self, 'active', True), self.game)
            if self.active:
                self.draw(surface)
        else:
            self.waiting = False
            self.active = False
            if self.timer:
                self.timer.discard()
            
    def draw(self, surface):
        text_image = self.description.image
        pos = pygame.Vector2(550, -75)
        padding = pygame.Vector2(188, 188)

        surface.blit(self.dialog, pos)
        surface.blit(text_image, pos + padding)
	