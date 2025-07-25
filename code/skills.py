from setting import *

class Skill:
    def __init__(self, user, game):
        # Weapon related
        self.user = user
        self.game = game
        
        # States
        self.ready = False
        self.casting = False
        
        # Stats
        self.cooldown, self.warmup, self.cast_time = skill_stats[self.name]
        self.remaining = self.warmup
        
        # Passive = not depends on user states
        self.passive = False
        
        # Audio
        if self.name in game.skill_audio:
            self.sound = game.skill_audio[self.name]
    
    def play_sound(self):
        if hasattr(self, 'sound'):
            self.sound.play()
    
    def cast(self):
        if self.passive:
            self.activate()
            return
        
        if self.ready and not self.user.stunned and not self.user.silenced and not self.user.channeling and not self.user.meditating:
            self.activate()
        else:
            self.warning()

    def activate(self):
        self.play_sound()
        self.ready = False
        self.casting = True
        self.remaining = self.cast_time

    def deactivate(self):
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
        

