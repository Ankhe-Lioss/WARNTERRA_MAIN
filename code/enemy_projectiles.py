from projectiles import *
from status import *

class Karthus_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Karthus Primary'
        self.wall_piercing = True
        super().__init__(user, direction, game)

class Veigar_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Primary'
        super().__init__(user, direction, game)
        self.rect.inflate(-30, -30)

class Veigar_Secondary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Secondary'
        super().__init__(user, direction, game)
        self.rect.inflate_ip(-30, -30)

class Veigar_Ult(Enemy_projectiles):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.source='Veigar Ult'
        super().__init__(user, pygame.Vector2(0, 0), game)
        self.rect = self.image_rect.inflate(-20, -20)
        self.wall_piercing = True
        self.lifetime = 20000
    
    def update(self, dt):
        # Track the player
        self.direction = pygame.Vector2(self.game.player.rect.center) - pygame.Vector2(self.rect.center)
        self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction
        super().update(dt)
    
    def collide(self, sprite):
        sprite.take_damage(sprite.maxhp * 0.5, pen=0.5, type="normal")
        self.play_sound()

class Lulu_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Lulu Primary'
        super().__init__(user, direction, game)
    
    def apply(self, target):
        target.status.add(Slowed(3000, 0.5, self.game, target))