from setting import *
from entities import *
from player import Player
from groups import *
from setlevel import *
from cursor import *
from weapon import *

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
        
        # Statew
        self.running = True
        self.pausing = False
        
        # Groups
        self.all_sprites = AllSprites()
        self.player_sprites = pygame.sprite.GroupSingle()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Player
        setlevel(self)
        
        # Testing
        
        
    
    def run(self):
        while self.running:
            
            # Data time
            dt = self.clock.tick(FPS) / 1000
            
            # Get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # FILL
            self.display_surface.fill('darkgray')
            
            # TESTING AREA
            self.all_sprites.draw(self.player.rect)
            self.all_sprites.update(dt)

            # CURSOR
            cursor(game)

            # UPDATE (LAST)
            pygame.display.update()
        # Cútd
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()