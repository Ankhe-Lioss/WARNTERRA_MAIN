from entity import Enemy
from enemy_skills import *

class Poro(Enemy):
    def __init__(self, pos, game):
        self.name='Poro'
        super().__init__(pos, game)
        self.rect = self.rect.inflate(-30, -30)
        self.skills = {
            'primary': Poro_stomp(self, game),
        }
        self.ghost = True

class Meele(Enemy):
    def __init__(self, pos, game):
        self.name='Meele'
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        
class Karthus(Enemy):
    def __init__(self, pos, game):
        self.name='Karthus'
        super().__init__(pos, game)
        self.rect = self.rect.inflate(-20, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            "primary" : Karthus_primary(self, game)
        }
        
class Chogath(Enemy):
    def __init__(self, pos, game):
        self.name='Chogath'
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            "primary" : Chogath_stomp(self, game)
        }

        