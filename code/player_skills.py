from skills import Skill
from setting import *
import player_projectiles as pproj

class Gauntlet_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_primary(self.user.rect.center, self.user.facing_dir, self.game)

class Gauntlet_q_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        print(self.remaining)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_q_skill(self.user.rect.center, self.user.facing_dir, self.game)

class Gauntlet_e_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()        
        self.user.channeling = True
        self.bow = pproj.Gauntlet_e_skill(self.user.rect.center, self.user.facing_dir, self.game)
        
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

class Bow_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bow_primary(self.user.rect.center, self.user.facing_dir, self.game)
    
class Bow_secondary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.weap.primary = Bow_primary_enhanced(self.user, self.game)
    
    def deactivate(self):
        super().deactivate()
        self.user.weap.primary = Bow_primary(self.user, self.game)

class Bow_primary_enhanced(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        
        shooting_pos = self.user.rect.center
        shooting_dir = self.user.facing_dir
        
        pproj.Bow_primary_enhanced(shooting_pos, shooting_dir, self.game)
        pproj.Bow_primary_enhanced(shooting_pos + shooting_dir.rotate(135) * 25, shooting_dir, self.game)
        pproj.Bow_primary_enhanced(shooting_pos + shooting_dir.rotate(-135) * 25, shooting_dir, self.game)
    
class Bow_q_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        
        pos = self.user.rect.center
        dir = self.user.facing_dir
        
        pproj.Bow_q_skill(pos, dir, self.game)
        pproj.Bow_q_skill(pos, dir.rotate(10), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(-10), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(20), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(-20), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(30), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(-30), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(40), self.game)
        pproj.Bow_q_skill(pos, dir.rotate(-40), self.game)
    
    def deactivate(self):
        super().deactivate()

class Bow_e_skill(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)