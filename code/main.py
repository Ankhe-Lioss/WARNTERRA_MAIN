from setting import *
from enemies import *

# THIS FKING MAIN GAME SIHFHFHFHFHFHFHFHF
class Game:
    def __init__(self):
        # Initializing
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # Testing
        self.player = "iusdguyfsgduyfgsuydfgsudfgyusgfuysdgufgsufyd"
        self.enemy_level = 0
        self.pr = Poro((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), enemy_stat["Poro"], (self.all_sprites, self.enemy_sprites), self)
        
        
        
    def run(self):
        while self.running:
            # Data time
            dt = self.clock.tick(FPS) / 1000
            
            # Get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.display_surface.fill('darkgray')
            self.display_surface.blit(self.pr.image,(0, 0)) 
    
            pygame.display.update()
        # Cút
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()