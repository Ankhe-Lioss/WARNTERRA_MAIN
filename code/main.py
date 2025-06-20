import pygame

from setting import *
from groups import AllSprites
from setlevel import *
from cursor import *
from button import *


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
        self.pausing = False
        # Groups
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
        # game load asset
        load_menu(self)

        self.game_state = 'in_game'
        self.menu_state = 'main'

    def run(self):
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
                    if event.key == pygame.K_F11 and self.screen_toggle - self.clock.get_time() < -5:
                        pygame.display.toggle_fullscreen()
                        self.screen_toggle = self.clock.get_time()

            # FILL
            self.display_surface.fill('gray36')

            # Enemies Spawning
            check_game_state(self)

            # Game State
            self.all_sprites.draw(self.player.rect)
            if not self.pausing:
                self.all_sprites.update(dt)
            else:
                self.draw_menu()
            # CURSOR
            cursor(game)

            # UPDATE (LAST)
            pygame.display.update()
        # Cútd
        pygame.quit()

    def draw_menu(self):
        if self.pausing:
            # Optional dark overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(100)
            overlay.fill((255, 255, 255))
            self.display_surface.blit(overlay, (0, 0))

            if self.menu_state == "main":
                if self.resume_button.draw(self.display_surface):
                    self.pausing = False
                if self.options_button.draw(self.display_surface):
                    self.menu_state = "options"
                if self.quit_button.draw(self.display_surface):
                    self.running = False

            elif self.menu_state == "options":
                if self.video_button.draw(self.display_surface):
                    print("Video Settings")
                if self.audio_button.draw(self.display_surface):
                    print("Audio Settings")
                if self.keys_button.draw(self.display_surface):
                    print("Change Key Bindings")
                if self.back_button.draw(self.display_surface):
                    self.menu_state = "main"

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x, y))


if __name__ == "__main__":
    game = Game()
    game.run()