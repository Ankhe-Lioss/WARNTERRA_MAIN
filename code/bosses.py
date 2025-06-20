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
            'ult': Veigar_ult(self, game),
        }