from setting import *

class Status(pygame.sprite.Sprite):
    def __init__(self, duration, game):
        self.remaining = duration
        self.game = game
        super().__init__(game.all_sprites)
        
        self.image = pygame.surface.Surface(size=(0, 0))
        self.rect = pygame.rect.FRect()

    def unapply(self):
        pass

    def update(self, dt):
        self.remaining -= dt * 1000
        if self.remaining <= 0:
            self.unapply()
            self.kill()
            
            

class Stunned(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.owner.stunned = True

    def unapply(self):
        self.owner.stunned = False

class Poisonned(Status):
    def __init__(self, duration, dps, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.dps = dps
    
    def update(self, dt):
        super().update(dt)
        self.owner.take_damage(self.dps / dt, type="dot")