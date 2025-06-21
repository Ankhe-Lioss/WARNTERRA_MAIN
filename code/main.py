import pygame

from setting import *
from groups import AllSprites
from setlevel import *
from cursor import *
from button import *
from background import *

# THIS FKING MAIN GAME SIHFHFHFHFHFHFHFHF
class Game:
    def __init__(self):
        # Initializing
        pygame.init()

        # Display
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(False)

        # Caption
        pygame.display.set_caption("Warnterra 1.0")

        # Times
        self.clock = pygame.time.Clock()
        # States
        self.running = True

        # game load asset
        load_menu(self)
        check_cursor(self)

        self.game_state = 'in_start_menu'
        self.menu_state = 'main'
        self.pausing = True
        self.background = Background()
    def restart(self):  # Groups
        self.all_sprites = AllSprites()
        self.player_sprites = pygame.sprite.GroupSingle()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Stat for levels

        self.spawn_numb = 0
        self.checked_in = True
        self.room = 0
        self.wave = 0
        self.screen_toggle = 0
        self.level = 3
        self.state = 'in_level'
        setlevel(self)
    def run(self):
        self.restart()
        while self.running:
            # Data time
            dt = self.clock.tick(FPS) / 1000

            # Get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pausing = not self.pausing
                    if event.key == pygame.K_F11 and self.screen_toggle - pygame.time.get_ticks() < -5000:
                        pygame.display.toggle_fullscreen()
                        self.screen_toggle = pygame.time.get_ticks()
                    if event.key == pygame.K_F1:
                        self.player.death()
                    if event.key == pygame.K_F2:
                        self.player.atk=10000000
                        self.player.hp=1000000
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        self.pausing = not self.pausing
            # FILL
            self.display_surface.fill('gray36')

            # Enemies Spawning
            check_game_state(self)

            # Game State
            self.all_sprites.draw(self.player.rect)
            if not self.pausing:
                self.all_sprites.update(dt)

            self.draw_menu(dt)
            # CURSOR
            check_cursor(self)

            # UPDATE (LAST)
            pygame.display.update()
        # Cútd
        pygame.quit()

    def draw_menu(self,dt):
        if self.pausing and self.game_state == 'in_game':
            self.pause_menu()
        if self.game_state == 'in_start_menu':
            self.background.draw(dt,self.display_surface)
            self.start_menu()
        if self.game_state == 'in_death_menu':
            self.death_menu()
        if self.pausing or not(self.game_state == 'in_game'):
            if self.have_joystick:
                # A button (Restart)
                if self.joystick.get_button(0):
                    self.restart()
                    self.pausing = False
                    self.game_state = 'in_game'
                # X button (Quit)
                if self.joystick.get_button(2):
                    self.running = False

                # B button (Back to Start Menu)
                if self.joystick.get_button(1):
                    self.game_state = "in_start_menu"
    def start_menu(self):
        if self.menu_state == 'main':
            if self.start_button.draw(self.display_surface):
                self.restart()
                self.game_state = "in_game"
                self.pausing = False
            if self.quit_start_button.draw(self.display_surface):
                self.running = False
            if self.options_button.draw(self.display_surface):
                self.menu_state = "options"
        if self.menu_state == "options":
            if self.video_button.draw(self.display_surface):
                print("Video Settings")
            if self.audio_button.draw(self.display_surface):
                print("Audio Settings")
            if self.keys_button.draw(self.display_surface):
                print("Change Key Bindings")
            if self.back_button.draw(self.display_surface):
                self.menu_state = "main"

    def pause_menu(self):
        # Optional dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.display_surface.blit(overlay, (0, 0))


        if self.resume_button.draw(self.display_surface):
            self.pausing = False

        if self.quit_button.draw(self.display_surface):
            self.running = False
        if self.restart_button.draw(self.display_surface):
            self.restart()
            self.pausing = False
        if self.startmenu_button.draw(self.display_surface):
            self.game_state = "in_start_menu"

    def death_menu(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0,0))
        self.display_surface.blit(overlay, (0, 0))
        self.display_surface.blit(self.deathmenu_img, (183, 120))
        if self.death_to_quit_button.draw(self.display_surface):
            self.running = False
        if self.death_to_start_button.draw(self.display_surface):
            self.game_state = "in_start_menu"
        if self.death_to_restart_button.draw(self.display_surface):
                self.restart()
                self.game_state = "in_game"
                self.pausing = False
if __name__ == "__main__":
    game = Game()
    game.run()