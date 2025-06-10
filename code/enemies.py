from entities import Enemy
from enemy_skills import *

class Poro(Enemy):
    def __init__(self, pos, groups, game):
        self.name='Poro'
        super().__init__(pos,groups,game)
        self.rect = self.rect.inflate(0, 0)
        self.primary=Poro_stomp(self, game)
        self.skills.append(self.primary)

class Meele(Enemy):
    def __init__(self, pos,groups, game):
        self.name='Meele'
        super().__init__(pos,groups,game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        
class Karthus(Enemy):
    def __init__(self, pos,groups, game):
        self.name='Karthus'
        super().__init__(pos,groups,game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.primary = Karthus_primary(self, game)
        self.skills.append(self.primary)
        
class Chogath(Enemy):
    def __init__(self, pos,groups, game):
        self.name='Chogath'
        super().__init__(pos,groups,game)
        self.rect = self.rect.inflate(0, 0)
        self.asymmetry=True
        self.attack_time=1000
        self.primary = Chogath_stomp(self, game)
        self.skills.append(self.primary)