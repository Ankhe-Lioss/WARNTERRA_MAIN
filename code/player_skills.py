from skills import Skill
from setting import *
import player_projectiles as pproj

class Gauntlet_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_primary(self.user.rect.center, self.user.facing_dir, (self.game.player_projectiles, self.game.all_sprites), self.game)

class Gauntlet_q_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        print(self.remaining)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_q_skill(self.user.rect.center, self.user.facing_dir, (self.game.player_projectiles, self.game.all_sprites), self.game)

class Gauntlet_e_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()        
        self.user.channeling = True
        self.bow = pproj.Gauntlet_e_skill(self.user.rect.center, self.user.facing_dir, (self.game.player_projectiles, self.game.all_sprites), self.game)
        
    def deactivate(self):
        super().deactivate()
        self.bow.spd = player_projectiles["Gauntlet_e_skill"][1]
        self.user.channeling = False

class Gauntlet_secondary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.mode = {"dir" : self.user.facing_dir.copy(), "spd" : 2000}
        self.user.forced_moving = True
        
    def deactivate(self):
        super().deactivate()
        self.user.mode = None
        self.user.forced_moving = False

        