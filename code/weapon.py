from setting import *
from skills import *

class weap(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.game = game
        
        # Init
        self.image = pygame.image.load(os.path.join('images', 'weapon', f"{self.name}.png")).convert_alpha()
        self.image_rect = self.image.get_frect(center=self.game.player.hitbox_rect.center)
        
        
        
    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.primary.execute()
        if pygame.mouse.get_pressed()[2]:
            self.secondary.execute()
        if pygame.key.get_pressed()[pygame.K_q]:
            self.q_skill.execute()
        if pygame.key.get_pressed()[pygame.K_e]:
            self.e_skill.execute()

class Gauntlet(weap):
    def __init__(self, groups, game):
        super().__init__(player_skills["Gauntlet"])
        