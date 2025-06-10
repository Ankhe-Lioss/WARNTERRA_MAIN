from projectiles import *

class Karthus_Primary(Enemy_projectiles):
    def __init__(self, user, direction, groups,game):
        self.name = self.__class__.__name__
        self.source='Karthus Primary'
        self.piercing = True
        super().__init__(user, direction, groups, game)
