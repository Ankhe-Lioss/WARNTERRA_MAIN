from setting import *
from entity import Boss
from enemy_skills import *

class Veigar(Boss):
    def __init__(self, groups, game):
        self.name = 'Veigar'
        super().__init__(groups, game)
        self.skills = {
            'primary': Veigar_primary(self, game),
            'secondary': Veigar_secondary(self, game),
        }
        self.mode = 1
        self.phase = 1
        self.phase_remaining = 10000
    
    def change_phase(self):
        super().change_phase()
        self.skills = {
            'secondary' : Veigar_secondary(self, self.game),
            'ult': Veigar_ult(self, self.game),
        }
        self.skills['secondary'].warmup = 1000
        self.skills['secondary'].cooldown = 2000
        self.phase = 2
        self.mode = 1
    
    def update(self, dt):
        super().update(dt)
        self.phase_remaining -= dt * 1000
        if self.mode == 1 and self.phase_remaining <= 0: # 1 to 2
            self.mode = 2
            if self.phase == 1:
                del self.skills['primary']
                del self.skills['secondary']
                self.skills['aoe'] = Veigar_aoe(self, self.game)
                
                self.phase_remaining = 6000
            else:
                del self.skills['secondary']
                self.skills['aoe'] = Veigar_aoe(self, self.game)
                self.skills['cage'] = Veigar_cage(self, self.game)
                
                self.phase_remaining = 6000
                
        elif self.mode == 2 and self.phase_remaining <= 0:
            self.mode = 1
            if self.phase == 1:
                del self.skills['aoe']
                self.skills['primary'] = Veigar_primary(self, self.game)
                self.skills['secondary'] = Veigar_secondary(self, self.game)
                
                self.phase_remaining = 10000
                
            else:
                del self.skills['aoe']
                del self.skills['cage']
                self.skills['secondary'] = Veigar_secondary(self, self.game)
                self.skills['secondary'].cooldown = 1000
                
                self.phase_remaining = 10000