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
        self.keep_range = self.stats[8]
        
        self.updstat()
        
        #states
        self.channeling = False
        self.forced_moving = False
        self.stunned = False
        self.mode = None
        self.silenced = False
        self.ghost = False
        self.rooted = False
        self.cross_wall = False
        
        # Status
        self.status = set()
        
        self.rect = pygame.rect.FRect()
        
        self.healthbar = Healthbar(self)
        
    def updstat(self):
        self.maxhp = self.raw_hp + self.level * self.hp_multiplier
        self.baseatk = self.raw_atk + self.level * self.atk_multiplier
        self.basedef = self.raw_def + self.level * self.def_multiplier
        
        self.hp = self.maxhp
        self.atk = self.baseatk
        self.def_ = self.basedef
        self.spd = self.basespd

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
        if dmg < 0:
            dmg = 0    
    
        delta = dmg / (1 + 0.01 * self.def_ * (1 - pen))
        self.hp -= delta
        
        if type == "normal":
            Flyout_number(self.rect.center, int(delta), (200, 0, 0), self.game)
        
        if type == "DoT":
            Flyout_number(self.rect.center, int(delta), (0, 165, 0), self.game, font_size=20)
        
        if self.hp <= 0:
            self.death()
        
    def heal(self, healing, type="normal"):
        if type == "normal":
            Flyout_number(self.rect.center, "+" + str(int(healing)), (100, 255, 100), self.game)
        elif type == "overtime":
            Flyout_number(self.rect.center, "+" + str(int(healing)), (100, 255, 100), self.game, font_size=20)
        self.hp = min(self.hp + healing, self.maxhp)
    
    def death(self):
        for stt in self.status:
            stt.kill()
        self.kill()
    
    def move(self, dt):
        if self.channeling or self.stunned or self.rooted:
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        if not self.cross_wall:
            self.collision('horizontal', self.direction)
        
        self.rect.y += self.direction.y * self.spd * dt
        if not self.cross_wall:
            self.collision('vertical', self.direction)
        
        self.image_rect.center = self.rect.center
    
    def forced_move(self, dir, dt):
        if self.rooted or self.stunned:
            return
        
        forced_spd = self.mode["spd"]
        
        
        self.rect.x += dir.x * forced_spd * dt
        if not self.cross_wall:
            self.collision('horizontal', dir)
            
        self.rect.y += dir.y * forced_spd * dt
        if not self.cross_wall:
            self.collision('vertical', dir)
            
        self.image_rect.center = self.rect.center
    
    def update(self, dt):
        if self.forced_moving:
            self.forced_move(self.mode["dir"], dt)
        else:
            self.move(dt) 
    
    def update_stat(self):
        pass

class Flyout_number(pygame.sprite.Sprite):
    
    def __init__(self, pos, number, color, game, font_size=24):
        super().__init__(game.all_sprites)
        self.image = pygame.font.Font(None, font_size).render(str(number), True, color)
        self.image_rect = self.image.get_frect(center=pos)
        self.lifetime = 0.5
        self.spawn_time = pygame.time.get_ticks()
        self.type = 'top'
    
    def update(self, dt):
        elapsed_time = pygame.time.get_ticks() - self.spawn_time
        if elapsed_time < self.lifetime * 1000:
            self.image_rect.y -= 50 * dt
            alpha = max(0, 255 - int((elapsed_time / (self.lifetime * 1000)) * 255))
            self.image.set_alpha(alpha)
        else:
            self.kill()

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
        self.skills = {}
        
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
        self.image_rect = self.rect.copy()
    
    def load_frames(self):
        self.frames = {}
        for i in self.states:
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
        self.game.spawn_numb -= 1
        
    def cal_dis(self):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.distance_vector = player_pos - enemy_pos
        self.direction = self.distance_vector.normalize() if self.distance_vector else self.distance_vector
        
    def move_enemy(self,dt):
        # update the rect position + collision
        
        if self.forced_moving:
            self.forced_move(self.mode['dir'], dt)
            return
        
        if self.channeling or self.stunned or self.forced_moving or self.rooted:
            return
        
        distance = self.distance_vector.length()
        if distance <= self.keep_range:
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        if not self.cross_wall:
            self.collision('horizontal', self.direction)
        self.enemy_collision('horizontal',dt)
        self.rect.y += self.direction.y * self.spd * dt
        
        if not self.cross_wall:
            self.collision('vertical', self.direction)
        self.enemy_collision('vertical',dt)
        self.image_rect.center = self.rect.center
        
    def enemy_collision(self,direction,dt):
        for sprite in self.game.enemy_sprites:
                if self!=sprite:
                    if sprite.rect.colliderect(self.rect):
                        if direction == 'horizontal':
                            self.rect.x -= self.direction.x * self.spd * dt
                        else:
                            self.rect.y -= self.direction.y * self.spd * dt

    def attacking(self):
        if self.distance_vector.length() <= self.atk_range:
            for skill in self.skills:
                if self.skills[skill].ready:
                    self.skills[skill].cast()
                    
    def update(self, dt):
        if self.death_time==0:
            if len(self.status)!=0:
                #check_status(self,dt)
                pass
            self.cal_dis()
            for skill_name in self.skills:
                self.skills[skill_name].update(dt)
            self.attacking()
            self.move_enemy(dt)
            self.animate(dt)
        else:
            self.death_timer()

class Boss(Enemy):
    def __init__(self, pos, game):
        super().__init__(pos, game)
        
        # Boss specific attributes
        self.phase = 1
        self.phase_change_hp = 0.5 * self.maxhp  # Change phase at 50% HP
        self.special_skills = []  # List of special skills for the boss

    def update(self, dt):
        super().update(dt)
        if self.hp <= self.phase_change_hp and self.phase == 1:
            self.phase = 2
            self.change_phase()

    def change_phase(self):
        # Logic to change the boss's behavior or appearance when changing phases
        pass
