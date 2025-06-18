from projectiles import *
from status import *

class Gauntlet_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)

class Gauntlet_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.target, False, pygame.sprite.collide_mask)
        if collision_sprites:
            
            self.game.player.weap.q_skill.remaining -= 2000
            self.game.player.weap.e_skill.remaining -= 2000
            
            for sprite in collision_sprites:
                    sprite.take_damage(self.dmg)
                    self.play_sound()
                    self.kill()

class Gauntlet_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet SkillR"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.wall_piercing = True
        self.e_piercing = True
    
    def apply(self, target):
        target.status.add(Slowed(2000, 0.75, self.game, target))

class Bow_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)

class Bow_primary_enhanced(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def apply(self, target):
        target.status.add(Slowed(500, 0.3, self.game, target))

class Bow_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillQ"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def apply(self, target):
        target.status.add(Slowed(1500, 0.6, self.game, target))

class Bow_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillE"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def apply(self, target):
        target.status.add(Stunned(5000, self.game, target))