from setting import *
from skills import *

class Weap(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.game = game
        self.player = game.player
        
        # Init
        self.image = pygame.image.load(os.path.join('images', 'weapon', f"{self.name}.png")).convert_alpha()
        self.rect = self.image.get_frect(center=self.game.player.hitbox_rect.center)
        
        # Import skills
        
    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.primary.cast()
        if pygame.mouse.get_pressed()[2]:
            self.secondary.cast()
        if pygame.key.get_pressed()[pygame.K_q]:
            self.q_skill.cast()
        if pygame.key.get_pressed()[pygame.K_e]:
            self.e_skill.cast()
    
    def update(self, dt):
        self.input()
        self.primary.update(dt)

class Gauntlet(Weap):
    def __init__(self, groups, game):
        self.name = self.__class__.__name__
        super().__init__(groups, game)
        
        # Import skills
        self.primary = Gauntlet_primary(self)
        