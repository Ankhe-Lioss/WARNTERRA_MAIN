from setting import *
from health_bar import Healthbar

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        
        #initialize sprite
        super().__init__((groups, game.all_sprites))
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
        self.atk_range = self.stats[7]
        
        self.updstat()
        
        self.hp = self.maxhp
        self.atk = self.baseatk
        self.def_ = self.basedef
        self.spd = self.basespd
        
        #states
        self.channeling = False
        self.forced_moving = False
        self.stunned = False
        self.mode = None
        self.silent = False
        
        # Status
        self.status = set()
        
        self.rect = pygame.rect.FRect()
        
        self.healthbar = Healthbar(self)
        
    def updstat(self):
        self.maxhp = self.raw_hp + self.level * self.hp_multiplier
        self.baseatk = self.raw_atk + self.level * self.atk_multiplier
        self.basedef = self.raw_def + self.level * self.def_multiplier

    def collision(self, dir_type, dir):
        for sprite in self.game.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if dir_type == 'horizontal':
                    if dir.x > 0: self.rect.right = sprite.rect.left
                    if dir.x < 0: self.rect.left = sprite.rect.right
                else:
                    if dir.y < 0: self.rect.top = sprite.rect.bottom
                    if dir.y > 0: self.rect.bottom = sprite.rect.top
    
    def take_damage(self, dmg, pen = 0, type="normal"):
        self.hp -= dmg / (1 + 0.01 * self.def_ * (1 - pen))
        if self.hp <= 0:
            self.death()
        
    def heal(self, healing):
        self.hp = min(self.hp + healing, self.maxhp)
    
    def death(self):
        self.kill()
    
    def move(self, dt):
        if self.channeling or self.stunned:
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        self.collision('horizontal', self.direction)
        self.rect.y += self.direction.y * self.spd * dt
        self.collision('vertical', self.direction)
    
    def forced_move(self, dir, dt):
        forced_spd = self.mode["spd"]
        self.rect.x += dir.x * forced_spd * dt
        self.collision('horizontal', dir)
        self.rect.y += dir.y * forced_spd * dt
        self.collision('vertical', dir)
    
    def update(self, dt):
        if self.forced_moving:
            self.forced_move(self.mode["dir"], dt)
        else:
            self.move(dt) 
    
    def update_stat(self):
        pass

class Enemy(Entity):
    def __init__(self, pos, game):
        # Initializing
        super().__init__(game.enemy_sprites, game)
        self.player = self.game.player
        
        # Animation FPS
        self.animation_spd = 6
        
        # On-death
        self.death_time = 0
        self.death_duration = 0.5
        
        # Skill
        self.skills = []
        
        # State
        self.frame_index = 0
        self.states=['Walking', 'Attacking']
        self.state='Walking'
        
        #load image
        self.load_frames()
        
        # image
        self.image = self.frames['Walking'][0]
        
        # rect
        self.rect = self.image.get_frect(center=pos)
    
    def load_frames(self):
        self.frames = {}
        for i in self.states :
            self.frames[i] = []
            for k in range(0, 6):
                surf = pygame.image.load(os.path.join('images', 'enemies',f'{self.name}',f'{i}',f'{k}.png')).convert_alpha()
                self.frames[i].append(surf)
    
    def animate(self, dt):
        self.frame_index += self.animation_spd * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        if hasattr(self, 'asymmetry') and self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def death(self):
        super().death()
        
    def cal_dis(self):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.distance=player_pos-enemy_pos
        self.direction = self.distance.normalize() if self.distance else self.distance
        
    def move_enemy(self,dt):
        # update the rect position + collision
        
        if self.channeling:
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        self.collision('horizontal', self.direction)
        self.enemy_collision('horizontal',dt)
        self.rect.y += self.direction.y * self.spd * dt
        self.collision('vertical', self.direction)
        self.enemy_collision('vertical',dt)
        
    def enemy_collision(self,direction,dt):
        for sprite in self.game.enemy_sprites:
                if self!=sprite:
                    if sprite.rect.colliderect(self.rect):
                        if direction == 'horizontal':
                            self.rect.x -= self.direction.x * self.spd * dt
                        else:
                            self.rect.y -= self.direction.y * self.spd * dt
    def destroy(self):
        self.death_time=pygame.time.get_ticks()
        destroy_surf=pygame.mask.from_surface(self.frames['Walking'][0]).to_surface()
        destroy_surf.set_colorkey('black')
        self.image=destroy_surf
        
    def death_timer(self):
        if pygame.time.get_ticks()-self.death_time>=self.death_duration:
            self.kill()
            
    def attacking(self):
        if self.distance.length() <= self.atk_range:
            for skill in self.skills:
                if skill.ready:
                    skill.cast()
                    
    def update(self, dt):
        if self.death_time==0:
            if len(self.status)!=0:
                #check_status(self,dt)
                pass
            self.cal_dis()
            for skill in self.skills:
                skill.update(dt)
            self.attacking()
            self.move_enemy(dt)
            self.animate(dt)
        else:
            self.death_timer()