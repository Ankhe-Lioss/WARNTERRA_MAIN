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
            'aoe' : Veigar_aoe(self, game),
            
        }
    
    def change_phase(self):
        super().change_phase()
        self.skills = {
            'secondary' : Veigar_secondary(self, self.game),
            #'cage' : Veigar_cage(self, game)
            'ult': Veigar_ult(self, self.game),
        }
        self.skills['secondary'].warmup = 1000
        self.skills['secondary'].cooldown = 2000