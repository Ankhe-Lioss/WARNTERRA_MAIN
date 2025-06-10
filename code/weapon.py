from setting import *
from player_skills import *

class Weap(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.game = game
        self.player = game.player
        
        # Init
        self.surf = pygame.image.load(os.path.join('images', 'weapon', f'{self.name}.png')).convert_alpha()
        self.image = self.surf
        self.rect = self.image.get_frect(center=self.player.rect.center)
        
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
    
    def rotate_gun(self):
        angle = degrees(atan2(self.player.facing_dir.x, self.player.facing_dir.y)) + 180
        self.image = pygame.transform.rotozoom(self.surf, angle, 1)
        self.rect.center = self.player.rect.center
    
    def update(self, dt):
        self.input()
        self.primary.update(dt)
        self.secondary.update(dt)
        self.q_skill.update(dt)
        self.e_skill.update(dt)
        
        self.rotate_gun()

class Gauntlet(Weap):
    def __init__(self, groups, game):
        self.name = self.__class__.__name__
        super().__init__(groups, game)
        
        # Import skills
        self.primary = Gauntlet_primary(self.player, self.game)
        self.q_skill = Gauntlet_q_skill(self.player, self.game)
        self.e_skill = Gauntlet_e_skill(self.player, self.game)
        self.secondary = Gauntlet_secondary(self.player, self.game)
        