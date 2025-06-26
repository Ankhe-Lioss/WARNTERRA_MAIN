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
        self.icon = pygame.transform.scale(self.icon, (48, 48))

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
        self.user.channeling = True
        self.pos, self.dir = self.user.rect.copy().center, self.user.facing_dir.copy()
        self.fake = pproj.Gauntlet_e_skill(self.pos, self.dir, self.game)
        self.fake.bullet_collision = lambda: None
        self.fake.spd = 0
        
    def deactivate(self):
        super().deactivate()
        self.fake.kill()
        pproj.Gauntlet_e_skill(self.pos, self.dir, self.game)
        self.user.channeling = False

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
        arrow = pproj.Bow_e_skill(self.user.rect.center, self.user.facing_dir, self.game)
        
class PlayerSkills:
    def __init__(self, user, game):
        self.user = user
        self.game = game
        self.skills_gauntlet = {
            "Left": Gauntlet_primary(user, game),
            "Right": Gauntlet_secondary(user, game),
            "Q": Gauntlet_q_skill(user, game),
            "E": Gauntlet_e_skill(user, game)            
        }
        
        # Bow Skills
        self.skills_bow = {
        "Left": Bow_primary(user, game),
        "Right": Bow_secondary(user, game),
        "Q": Bow_q_skill(user, game),
        "E": Bow_e_skill(user, game),
        }
