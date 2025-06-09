from setting import *

class Skill:
    def __init__(self, cooldown, weap, warmup = 0):
        # Weapon related
        self.weap = weap
        
        # States
        self.ready = True
        self.casting = False
        self.remaining = warmup
        
        # Stats
        self.cooldown = cooldown
        self.cast_time = 0
    
    def cast(self):
        if self.ready:
            self.activate()
        else:
            self.warning()
    
    def activate(self):
        self.ready = False
        self.casting = True
        self.remaining = self.cast_time
    
    def deactivate(self):
        self.casting = False
        self.remaining = self.cooldown
        
    def update(self, dt):
        self.remaining -= dt
        if self.remaining <= 0:
            if self.casting:
                self.deactivate()
            else:
                self.ready = True
        
    
    
    def warning(self):
        pass
        

class Gauntlet_Primary(Skill):
    def __init__(self):
        super().__init__(1000, "sdgfushgfu")
    
    def update(self):
        super().update()
        print(self.remaining)