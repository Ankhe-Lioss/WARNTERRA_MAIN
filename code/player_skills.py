from skills import Skill
from setting import *
import player_projectiles as pproj
from status import *
import aoe
import aoe_warning as aoew

class Player_skill(Skill):
    def __init__(self, user, game):
        super().__init__(user, game)
        self.icon = pygame.image.load(os.path.join("images", "icons", "Player_skills", f"{self.name}.png")).convert_alpha()

# Gauntlet

class Gauntlet_primary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_primary(self.user.rect.center, self.user.facing_dir, self.game)
        
        # Test
        #Poisoned(3000, 50, self.game, self.user)

class Gauntlet_q_skill(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Gauntlet_q_skill(self.user.rect.center, self.user.facing_dir, self.game)

class Gauntlet_e_skill(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()        
        self.user.meditating = True
        self.pos, self.dir = self.user.rect.copy().center, self.user.facing_dir.copy()
        self.fake = pproj.Gauntlet_e_skill(self.pos, self.dir, self.game)
        self.fake.bullet_collision = lambda: None
        self.fake.spd = 0
        
    def deactivate(self):
        super().deactivate()
        self.fake.kill()
        pproj.Gauntlet_e_skill(self.pos, self.dir, self.game)
        self.user.meditating = False

class Gauntlet_secondary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.mode = {"dir" : self.user.facing_dir.copy(), "spd" : 2000, "type" : "dash"}
        self.user.forced_moving = True
        
        # Test
        #self.user.heal(100)
        
    def deactivate(self):
        super().deactivate()
        self.user.mode = None
        self.user.forced_moving = False

# Bow

class Bow_primary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bow_primary(self.user.rect.center, self.user.facing_dir, self.game)
    
class Bow_secondary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.weap.primary = Bow_primary_enhanced(self.user, self.game)
    
    def deactivate(self):
        super().deactivate()
        self.user.weap.primary = Bow_primary(self.user, self.game)

class Bow_primary_enhanced(Player_skill):
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
    
class Bow_q_skill(Player_skill):
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

class Bow_e_skill(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bow_e_skill(self.user.rect.center, self.user.facing_dir, self.game)

# Bazooka

class Bazooka_primary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bazooka_primary(self.user.rect.center, self.user.facing_dir, self.game)

class Bazooka_primary_enhanced(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bazooka_primary_enhanced(self.user.rect.center, self.user.facing_dir, self.game)

class Bazooka_secondary(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        self.user.weap.primary = Bazooka_primary_enhanced(self.user, self.game)
        Buff(self.cast_time, 0.3, 'atk', self.game, self.user)
    
    def deactivate(self):
        super().deactivate()
        self.user.weap.primary = Bazooka_primary(self.user, self.game)

class Bazooka_q_skill(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        dir = pygame.Vector2(self.user.facing_dir)
        pproj.Bazooka_q_skill(self.user.rect.center, dir, self.game)
        pproj.Bazooka_q_skill(self.user.rect.center, dir.rotate(-30), self.game)
        pproj.Bazooka_q_skill(self.user.rect.center, dir.rotate(30), self.game)

class Bazooka_e_skill(Player_skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Bazooka_e_skill(self.user.rect.center, self.user.facing_dir, self.game)
        
# Lunar gun
class Calibrum_primary(Player_skill): # L Calibrum
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Calibrum_primary(self.user.rect.center, self.user.facing_dir, self.game)

class Infernum_primary(Player_skill): # L Infernum
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        pproj.Infernum_primary(self.user.rect.center, self.user.facing_dir, self.game)

class Lunar_swap(Player_skill): # R
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        self.user.channeling = True
        if self.user.weap.gun_type == "Calibrum":
            self.user.weap.gun_type = "Infernum"
            self.user.weap.primary = Infernum_primary(self.user, self.game)
            self.user.weap.q_skill = self.user.weap.q_skills[self.user.weap.gun_type]
        else:
            self.user.weap.gun_type = "Calibrum"
            self.user.weap.primary = Calibrum_primary(self.user, self.game)
            self.user.weap.q_skill = self.user.weap.q_skills[self.user.weap.gun_type]
    
    def deactivate(self):
        super().deactivate()
        self.user.channeling = False   

class Calibrum_skill(Player_skill): # Q Calibrum
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        self.user.meditating = True
    
    def deactivate(self):
        super().deactivate()
        pproj.Calibrum_skill(self.user.rect.center, self.user.facing_dir, self.game)
        self.user.meditating = False

class Infernum_skill(Player_skill): # Q Infernum
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        self.user.channeling = True
    
    def deactivate(self):
        super().deactivate()
        pproj.Infernum_skill(self.user.rect.center, self.user.facing_dir, self.game)
        pproj.Infernum_skill(self.user.rect.center, self.user.facing_dir.rotate(-20), self.game)
        pproj.Infernum_skill(self.user.rect.center, self.user.facing_dir.rotate(20), self.game)
        self.user.channeling = False
        
class Lunar_ult(Player_skill): # E
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        self.user.meditating = True
    
    def deactivate(self):
        super().deactivate()
        self.user.meditating = False
        pproj.Lunar_ult(self.user.rect.center, self.user.facing_dir, self.game, self.user.weap.gun_type)

# Crossbow


# Whisper