from projectiles import *

class Gauntlet_primary(Player_projectiles):
    def __init__(self, pos, direction, groups, game):
        self.source = "Gauntlet Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, groups, game)

class Gauntlet_q_skill(Player_projectiles):
    def __init__(self, pos, direction, groups, game):
        self.source = "Gauntlet Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, groups, game)

class Gauntlet_e_skill(Player_projectiles):
    def __init__(self, pos, direction, groups, game):
        self.source = "Gauntlet SkillR"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, groups, game)
        self.piercing = True
        self.spd = 0
   