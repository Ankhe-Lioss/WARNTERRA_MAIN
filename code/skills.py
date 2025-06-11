from setting import *

class Skill:
    def __init__(self, user, game):
        # Weapon related
        self.user = user
        self.game = game
        
        # States
        self.ready = True
        self.casting = False
        
        # Stats
        self.cooldown, self.warmup, self.cast_time = skill_stats[self.name]
        self.remaining = self.warmup
    
    def cast(self):
        if self.ready and not self.user.stunned and not self.user.silent:
            self.activate()
        else:
            self.warning()
    
    def asound(self): pass
    def dsound(self): pass
    
    def activate(self):
        self.asound()
        self.ready = False
        self.casting = True
        self.remaining = self.cast_time

    def deactivate(self):
        self.dsound()
        self.casting = False
        self.remaining = self.cooldown
        
    def update(self, dt):
        self.remaining -= dt * 1000
        if self.remaining <= 0:
            if self.casting:
                self.deactivate()
            else:
                self.ready = True
        

    def warning(self):
        pass
        

