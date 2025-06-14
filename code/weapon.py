from setting import *
from player_skills import *

class Weap(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.player = game.player
        
        # Init
        self.surf = pygame.image.load(os.path.join('images', 'weapon', f'{self.name}.png')).convert_alpha()
        self.image = self.surf
        self.image_rect = self.image.get_frect(center=self.player.image_rect.center)
        
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
        self.secondary.update(dt)
        self.q_skill.update(dt)
        self.e_skill.update(dt)
    

class Gauntlet(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)
        
        # Import skills
        self.primary = Gauntlet_primary(self.player, self.game)
        self.q_skill = Gauntlet_q_skill(self.player, self.game)
        self.e_skill = Gauntlet_e_skill(self.player, self.game)
        self.secondary = Gauntlet_secondary(self.player, self.game)

class Bow(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)
        
        # Import skills
        self.primary = Bow_primary(self.player, self.game)
        self.q_skill = Bow_q_skill(self.player, self.game)
        self.e_skill = Bow_e_skill(self.player, self.game)
        self.secondary = Bow_secondary(self.player, self.game)