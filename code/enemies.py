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

class Lulu(Enemy):
    def __init__(self, pos, game):
        self.name = self.__class__.__name__
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            "primary" : Lulu_primary(self, game),
            "buff" : Lulu_buff(self, game)
        }

class Soraka(Enemy):
    def __init__(self, pos, game):
        self.name = self.__class__.__name__
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            
        }

class Maokai(Enemy):
    def __init__(self, pos, game):
        self.name = self.__class__.__name__
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            
        }

class Nocturne(Enemy):
    def __init__(self, pos, game):
        self.name = self.__class__.__name__
        super().__init__(pos, game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.skills = {
            'sprint' : Nocturne_sprint(self, self.game)
        }
        self.attacked = False
        self.cross_wall = True