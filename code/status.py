from setting import *

class Status(pygame.sprite.Sprite):
    def __init__(self, duration, game):
        self.remaining = duration
        self.game = game
        super().__init__(game.all_sprites)

        self.scale_ratio = self.owner.rect.w / game.player.rect.w / 1.2
        self.frame_index = 0
        self.frames = []
        self.icon = None  # Static icon for UI

        self.load_images()
        self.load_icon()

        self.image = self.frames[self.frame_index]
        self.image_rect = self.image.get_frect(center=self.owner.rect.center)

    def load_images(self):
        self.frames = [pygame.transform.scale_by(surf, self.scale_ratio) for surf in
            self.game.status_frames[self.name]]

    def load_icon(self):
        icon_key = getattr(self, 'type', self.name)
        if hasattr(self.game, 'status_icons') and icon_key in self.game.status_icons:
            self.icon = self.game.status_icons[icon_key]
        else:
            self.icon = None

    def unapply(self):
        pass
    
    def cleanse(self):
        self.unapply()
        self.kill()

    def update_animation(self, dt):
        self.frame_index +=6*dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        
    def update_position(self):
        self.image_rect.center = pygame.Vector2(self.owner.rect.center) + self.offset * self.scale_ratio
        
    def update(self, dt):
        self.update_animation(dt)
        self.update_position()
        self.remaining -= dt * 1000
        if self.remaining <= 0:
            self.unapply()
            self.kill()
        if self.owner.hp<=0:
            self.kill()

class Aura(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        super().__init__(duration, game)
    
    def load_images(self):
        self.frames = [pygame.transform.scale_by(surf, self.scale_ratio) for surf in
            self.game.aura_frames[self.name]]
            
class Stunned(Status):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, -20)
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
            self.owner.take_damage(self.dps / 4, type="poison")

class Burning(Status):
    def __init__(self, duration, dps, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset=pygame.Vector2(0, -50)
        super().__init__(duration, game)
        self.dps = dps
        self.ticks = int(self.remaining) // 250
    
    def update(self, dt):
        super().update(dt)
        cur_tick = int(self.remaining) // 250
        if self.remaining > 0 and cur_tick != self.ticks:
            #print(self.remaining, self.ticks)
            self.ticks = cur_tick
            self.owner.take_damage(self.dps / 4, type="burning")

class Slowed(Status):
    def __init__(self, duration, ratio, game, owner):
        self.name = self.__class__.__name__
        self.offset=pygame.Vector2(0, -25)
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

    def update(self, dt):
        self.owner.silenced = True
        super().update(dt)

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
        self.offset=pygame.Vector2(0, -20)
        super().__init__(duration, game)

        self.type = type
        self.load_icon()

        self.ratio = ratio

        if type == 'atk':
            owner.atk *= 1 + ratio
        elif type == 'def':
            owner.def_ *= 1 + ratio
        elif type == 'spd':
            owner.spd *= 1 + ratio
    def update_position(self):

        self.image_rect.center=self.owner.rect.midbottom+self.offset
    def unapply(self):
        if self.type == 'atk':
            self.owner.atk /= 1 + self.ratio
        elif self.type == 'def':
            self.owner.def_ /= 1 + self.ratio
        elif self.type == 'spd':
            self.owner.spd /= 1 + self.ratio
            
class Dark_aura(Aura):
    def __init__(self, duration, game, owner):
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset = pygame.Vector2(1, 0)
        super().__init__(duration, game, owner)
        for frame in self.frames:
            frame.set_alpha(80)

class Calibrum_mark(Aura):
    def __init__(self, duration, game, owner):     
        self.name = self.__class__.__name__
        self.owner = owner
        self.offset = pygame.Vector2(1, 0)
        
        super().__init__(duration, game, owner)
        
        if not hasattr(self.owner, "calibrum_aura") or self.owner.calibrum_aura is None:
            self.owner.calibrum_aura = self
        else:
            self.owner.calibrum_aura.remaining = max(self.owner.calibrum_aura.remaining, duration)
            self.kill()
            return
        
    def update(self, dt):
        super().update(dt)
    
    def unapply(self):
        self.owner.calibrum_aura = None