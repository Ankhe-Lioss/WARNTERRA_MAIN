from setting import *

class Status(pygame.sprite.Sprite):
    def __init__(self, duration, game):
        self.remaining = duration
        self.game = game
        super().__init__(game.all_sprites)
        
        self.image = pygame.surface.Surface(size=(0, 0))
        self.image_rect = pygame.rect.FRect()

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
        
    def update(self, dt):
        self.owner.stunned = True
        super().update(dt)       

class Poisoned(Status):
    def __init__(self, duration, dps, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.dps = dps
        self.ticks = int(self.remaining) // 250
    
    def update(self, dt):
        super().update(dt)
        cur_tick = int(self.remaining) // 250
        if self.remaining > 0 and cur_tick != self.ticks:
            #print(self.remaining, self.ticks)
            self.ticks = cur_tick
            self.owner.take_damage(self.dps / 4, type="DoT")

class Slowed(Status):
    def __init__(self, duration, ratio, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.ratio = ratio
        self.owner.spd *= (1 - self.ratio)

    def unapply(self):
        self.owner.spd /= (1 - self.ratio)

class Silenced(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.owner.silenced = True

    def unapply(self):
        self.owner.silenced = False
        
class Healing(Status):
    def __init__(self, duration, hps, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.hps = hps
        self.ticks = int(self.remaining) // 250
    
    def update(self, dt):
        super().update(dt)
        cur_tick = int(self.remaining) // 250
        if self.remaining > 0 and cur_tick != self.ticks:
            #print(self.remaining, self.ticks)
            self.ticks = cur_tick
            self.owner.heal(self.hps / 4, type="overtime")
            
class Rooted(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        super().__init__(duration, game)
        self.owner = owner
        self.owner.rooted = True

    def unapply(self):
        self.owner.rooted = False
        
    def update(self, dt):
        self.owner.rooted = True
        super().update(dt)       