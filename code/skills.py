from setting import *
import projectiles as proj

class Skill:
    def __init__(self, weap):
        # Weapon related
        self.weap = weap
        
        # States
        self.ready = True
        self.casting = False
        
        # Stats
        self.cooldown, self.warmup, self.cast_time = skill_stats[self.name]
        self.remaining = self.warmup
    
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
        self.remaining -= dt * 1000
        if self.remaining <= 0:
            if self.casting:
                self.deactivate()
            else:
                self.ready = True
        

    def warning(self):
        pass
        

class Gauntlet_primary(Skill):
    def __init__(self, weap):
        self.name = self.__class__.__name__
        super().__init__(weap)
    
    def activate(self):
        super().activate()
        proj.Gauntlet_primary(self.weap.player.hitbox_rect.center, self.weap.player.facing_dir, (self.weap.game.player_projectiles, self.weap.game.all_sprites), self.weap.game)

