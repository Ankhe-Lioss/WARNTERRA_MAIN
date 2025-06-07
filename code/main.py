from setting import *
from enemies import *
from player import Player

# THIS FKING MAIN GAME SIHFHFHFHFHFHFHFHF
class Game:
    def __init__(self):
        # Initializing
        pygame.init()
        
        # Display
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Caption
        pygame.display.set_caption("Warnterra 1.0")
        
        # Time
        self.clock = pygame.time.Clock()
        
        # State
        self.running = True
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        
        # Player
        self.player = Player(pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), group=(self.all_sprites), game=self)
        
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
            self.player.get_state()
            self.player.draw()



            # UPDATE (LAST)
            pygame.display.update()
        # Cút
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()