from setting import *

class entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game):
        
        #initialize sprite
        super().__init__(groups)
        self.game = game
        self.level = game.level
        
        #stats
        self.stats = entity_stats[self.name]
        
        self.raw_hp = self.stats[0]
        self.raw_atk = self.stats[1]
        self.raw_def = self.stats[2]
        self.basespd = self.stats[3]
        self.hp_multiplier = self.stats[4]
        self.atk_multiplier = self.stats[5]
        self.def_multiplier = self.stats[6]
        
        self._updstat()
        
        self.hp = self.maxhp
        self.atk = self.baseatk
        self.def_ = self.basedef
        self.spd = self.basespd
        
        #position
        self.pos = pos
        
    def _updstat(self):
        self.maxhp = self.raw_hp + self.level * self.hp_multiplier
        self.baseatk = self.raw_atk + self.level * self.atk_multiplier
        self.basedef = self.raw_def + self.level * self.def_multiplier

    def collision(self, dir):
        for sprite in self.game.collision_sprites:
            if sprite.image_rect.colliderect(self.hitbox_rect):
                if dir == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.image_rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.image_rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.image_rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.image_rect.top
    
    def take_damage(self, dmg):
        self.hp -= dmg / (1 + 0.01 * self.def_)
        if self.hp <= 0:
            self.death()
        
    def heal(self, healing):
        self.hp = min(self.hp + healing, self.maxhp)
    
    def death(self):
        pass

class enemy(entity):
    def __init__(self, pos, groups, game):
        # Initializing
        super().__init__(pos, groups, game)
        self.player = self.game.player
        
        # Animation FPS
        self.animation_spd = 6
        
        # On-death
        self.death_time = 0
        self.death_duration = 0.5
        
        # State
        self.frame_index = 0
        self.states=['Walking']
        self.state='Walking'
        
        #load image
        self.frames = {}
        self.load_frames()
        
        # image
        self.image = self.frames['Walking'][0]
        
        # rect
        self.rect = self.image.get_frect(center=pos)
    
    def load_frames(self):
        for i in self.states:
            self.frames[i] = []
            for k in range(0, 6):
                surf = pygame.image.load(os.path.join('images', 'enemies',f'{self.name}',f'{i}',f'{k}.png')).convert_alpha()
                self.frames[i].append(surf)
    
    def death():
        super().death()
        

class Poro(enemy):
    def __init__(self, pos, groups, game):
        super().__init__(pos, groups, game)
        self.skills = ["Poro_stomp"]
        self.image = pygame.image.load(os.path.join('images', 'poro.png'))
        self.rect = self.image.get_frect(center=pos)