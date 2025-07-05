import pygame

from setting import *
from groups import AllSprites
from setlevel import *
from cursor import *
from button import *
from background import *
from UI import UI
from preload import *

# THIS FKING MAIN GAME SIHFHFHFHFHFHFHFHF
class Game:
    def __init__(self):
        # Initializing
        pygame.init()

        # Display
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(False)
        self.game_font = pygame.font.Font(os.path.join('images', 'font', 'oldenglishtextmt.ttf'), 40)
        
        # Captiona
        preload_all_image(self)
        pygame.display.set_caption("Warnterra")
        pygame.display.set_icon(self.icon)
        
        # Times
        self.clock = pygame.time.Clock()
        
        # States
        self.running = True
        
        # game load asset
        load_menu(self)
        #print(self.enemy_frames)
        check_cursor(self)

        self.frame_index = 0
        self.state = None
        self.game_state = 'in_start_menu'
        self.menu_state = 'main'
        self.pausing = True
        self.background = Background()
        self.current_BGM = None
        self.level = 1         #LEVEL

        self.level -= 1 

        #fps cal
        self.font = pygame.font.Font(None, 20)  # You can use your game font here
        self.lowest_fps = float('inf')
        self.fps_timer = 0
        self.fps_interval = 5
        self.displayed_lowest_fps = 0
        self.total_fps = 0
        self.frame_count = 0
        self.average_fps = 0
        
    def restart(self):
        self.all_sprites = AllSprites()
        self.player_sprites = pygame.sprite.GroupSingle()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.aoe_sprites = pygame.sprite.Group()
        self.player_currweapdict=[]
        self.delays = set()

        self.spawn_numb = 0
        self.checked_in = True
        self.room = 0
        self.wave = 0
        self.screen_toggle = 0
        self.state = 'in_level'

        setlevel(self)

        self.ui = UI(self, self.player, self.display_surface)

        # Set states to show weapon choosing menu
        self.game_state = "in_game"
        self.pausing = True
    def run(self):
        self.restart()
        self.game_state = "in_start_menu"
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
                        self.player.atk=1000
                        self.player.hp=100000
                        self.player.maxhp=100000
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        self.pausing = not self.pausing
            # FILL
            self.display_surface.fill('gray9')


            check_game_state(self)
            for delay in self.delays.copy():
                delay.update(dt)
            
            
            # REPEATING TESTS
            #print(self.spawn_numb)
            

            # Game State
            self.all_sprites.draw(self.player)
            if not self.pausing :
                self.all_sprites.update(dt,self.player)
                self.frame_index += dt*6
            if self.game_state == 'in_game':
                self.ui.update(dt)
            self.draw_menu(dt)
            # CURSOR
            check_cursor(self)
            
            # UPDATE (LAST)
            # UPDATE (LAST)
            self.show_fps(dt)
            pygame.display.update()
        # Cútd
        pygame.quit()
    def show_fps(self,dt):
        # --- FPS Monitoring ---
        current_fps = self.clock.get_fps()
        if current_fps > 0 and current_fps < self.lowest_fps:
            self.lowest_fps = current_fps

        self.total_fps += current_fps
        self.frame_count += 1

        self.fps_timer += dt
        if self.fps_timer >= self.fps_interval:
            self.displayed_lowest_fps = self.lowest_fps
            self.average_fps = self.total_fps / self.frame_count if self.frame_count > 0 else 0

            # Reset for next interval
            self.lowest_fps = float('inf')
            self.total_fps = 0
            self.frame_count = 0
            self.fps_timer = 0

        # --- Draw FPS info on screen ---
        fps_text = self.font.render(f"{current_fps:.1f} Lowest(5s): {self.displayed_lowest_fps:.1f} Avg(5s): {self.average_fps:.1f}", True, 'red')
        self.display_surface.blit(fps_text, (10, 10))

    def draw_menu(self,dt):


        if self.pausing and self.game_state == 'in_game' and self.menu_state == 'main':
            self.pause_menu()

        if self.game_state == 'in_start_menu':
            self.background.draw(dt,self.display_surface)
            self.start_menu()
        if self.game_state == 'in_death_menu':
            self.death_menu()
            wave_text = self.game_font.render(f"Level Reached: {self.level+1}", True, (20, 40, 0))
            wave_rect = wave_text.get_rect(topleft=(281, 520))  # Adjust Y as needed
            self.display_surface.blit(wave_text, wave_rect)
        if self.pausing or not(self.game_state == 'in_game'):
            if self.have_joystick:
                # A button (Restart)
                if self.joystick.get_button(0):
                    self.restart()
                    self.pausing = False
                    self.game_state = 'in_game'
                    self.menu_state = True
                    pygame.mixer.stop()
                # X button (Quit)
                if self.joystick.get_button(2):
                    self.running = False

                # B button (Back to Start Menu)
                if self.joystick.get_button(1):
                    self.game_state = "in_start_menu"
                    pygame.mixer.stop()

    def start_menu(self):
        self.start_menu_audio.play(-1)
        if self.menu_state == 'main' :
            game.display_surface.blit(self.title_img, (295, 8))
            if self.start_button.draw(self.display_surface):
                self.restart()
                self.pausing = False
                game.start_menu_audio.stop()
            if self.quit_start_button.draw(self.display_surface):
                self.running = False
            '''if self.options_button.draw(self.display_surface):
                self.menu_state = "options"
        if self.menu_state == "options":
            if self.video_button.draw(self.display_surface):
                print("Video Settings")
            if self.audio_button.draw(self.display_surface):
                print("Audio Settings")
            if self.keys_button.draw(self.display_surface):
                    ("Change Key Bindings")
            if self.back_button.draw(self.display_surface):
                self.menu_state = "main"'''

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
        
        self.current_BGM = 'death'
        pygame.mixer.music.stop()
        self.death_menu_audio.play(-1)
        if self.death_to_quit_button.draw(self.display_surface):
            self.running = False
        if self.death_to_start_button.draw(self.display_surface):
            self.game_state = "in_start_menu"
            self.death_menu_audio.stop()
        if self.death_to_restart_button.draw(self.display_surface):
                self.restart()
                self.game_state = "in_game"
                self.pausing = False
                self.death_menu_audio.stop()
                self.current_BGM = None
    """
    def weapon_choosing_menu(self):
        if self.have_joystick:
            if self.joystick.get_button(4):
                self.player.weap.kill()
                self.player.weap = Bow(self)
                self.pausing = False
                self.game_state = "in_game"
                self.menu_state = "main"
            elif self.joystick.get_button(5):
                self.player.weap.kill()
                self.player.weap = Gauntlet(self)
                self.pausing = False
                self.game_state = "in_game"
                self.menu_state = "main"
        if self.bow_button.draw(self.display_surface):
            self.player.weap.kill()
            self.player.weap = Bow(self)
            self.pausing = False
            self.game_state = "in_game"
            self.menu_state = "main"
            self.chosen_weap = Bow

        if self.gauntlet_button.draw(self.display_surface):
            self.player.weap.kill()
            self.player.weap = Gauntlet(self)
            self.pausing = False
            self.game_state = "in_game"
            self.menu_state = "main"
            self.chosen_weap = Gauntlet
    """
if __name__ == "__main__":
    game = Game()
    game.run()
