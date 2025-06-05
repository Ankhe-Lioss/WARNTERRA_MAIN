from setting import *

class enemy(pygame.sprite.Sprite):
    def __init__(self, pos, stats, groups, game):
        
        #initialize sprite
        super().__init__(groups)
        self.player = game.player
        self.level = game.enemy_level
        
        #stats
        self.raw_hp = stats[0]
        self.raw_atk = stats[1]
        self.raw_def = stats[2]
        self.basespd = stats[3]
        self.hp_multiplier = stats[4]
        self.atk_multiplier = stats[5]
        self.def_multiplier = stats[6]
        
        self.updstat()
        
        self.hp = self.maxhp
        self.atk = self.baseatk
        self.def_ = self.basedef
        self.spd = self.basespd
        
        #position
        self.pos = pos
        
        
    def updstat(self):
        self.maxhp = self.raw_hp + self.level * self.hp_multiplier
        self.baseatk = self.raw_atk + self.level * self.atk_multiplier
        self.basedef = self.raw_def + self.level * self.def_multiplier

class Poro(enemy):
    def __init__(self, pos, stats, groups, game):
        super().__init__(pos, stats, groups, game)
        self.skills = ["Poro_stomp"]
        self.image = pygame.image.load(os.path.join('images', 'poro.png'))
        self.rect = self.image.get_frect(center=pos)