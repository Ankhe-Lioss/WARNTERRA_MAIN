from setting import *

class Status(pygame.sprite.Sprite):
    def __init__(self, duration, game):
        self.remaining = duration
        self.game = game
        super().__init__(game.all_sprites)
        self.frame_index = 0
        self.frames=[]
        self.load_images()
        self.image =self.frames[self.frame_index]
        self.image_rect = self.image.get_rect(center=self.owner.rect.center)
        
    def load_images(self):
        for i in range(5):
            surf=pygame.image.load(os.path.join('images','status',f'{self.name}',f'{i}.png'))
            self.frames.append(surf)

    def unapply(self):
        pass

    def update_animation(self,dt):
        self.frame_index +=6*dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        
    def update_position(self):
        self.image_rect.center = pygame.Vector2(self.owner.image_rect.midbottom) + self.offset
        
    def update(self, dt):
        self.update_animation(dt)
        self.update_position()
        self.remaining -= dt * 1000
        if self.remaining <= 0:
            self.unapply()
            self.kill()

class Stunned(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, 0)
        super().__init__(duration, game)
        self.owner.stunned = True

    def unapply(self):
        self.owner.stunned = False
        
    def update(self, dt):
        self.owner.stunned = True
        super().update(dt)       

class Poisoned(Status):
    def __init__(self, duration, dps, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, 0)
        super().__init__(duration, game)
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
        self.offset=pygame.Vector2(0, -20)
        self.owner = owner
        super().__init__(duration, game)
        self.ratio = ratio
        self.owner.spd *= (1 - self.ratio)

    def unapply(self):
        self.owner.spd /= (1 - self.ratio)

class Silenced(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, 0)
        super().__init__(duration, game)
        self.owner.silenced = True

    def unapply(self):
        self.owner.silenced = False
        
class Healing(Status):
    def __init__(self, duration, hps, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, 0)
        super().__init__(duration, game)
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
        self.owner = owner
        self.offset=pygame.Vector2(0, 0)
        super().__init__(duration, game)
        self.owner.rooted = True

    def unapply(self):
        self.owner.rooted = False
        
    def update(self, dt):
        self.owner.rooted = True
        super().update(dt)       
        
class Buff(Status):
    def __init__(self, duration, ratio, type, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0,-15)
        super().__init__(duration, game)
        self.ratio = ratio
        self.type = type
        if type == 'atk':
            owner.atk *= 1 + ratio
        elif type == 'def':
            owner.def_ *= 1 + ratio
        elif type == 'spd':
            owner.spd *= 1 + ratio
    def update_position(self):

        self.image_rect.center=self.owner.image_rect.midbottom+self.offset
    def unapply(self):
        if self.type == 'atk':
            self.owner.atk /= 1 + self.ratio
        elif self.type == 'def':
            self.owner.def_ /= 1 + self.ratio
        elif self.type == 'spd':
            self.owner.spd /= 1 + self.ratio