from setting import *
from health_bar import Healthbar
from helper import *
from sprites import *

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
        self.channeling = False       # Cannot use skill (Only 1 at a time)
        self.forced_moving = False    # Sprinting
        self.stunned = False          # Cannot move and skill
        self.mode = None              # Optional (usually for forced moving)
        self.silenced = False         # Cannot use skill (Debuff status)
        self.ghost = False            # Go through enemies
        self.rooted = False           # Cannot move (Debuff status)
        self.cross_wall = False       # Not checking for wall collisions
        self.meditating = False       # Cannot move (Like channeling but also cannot move, only 1 at a time)
        
        #init rect for work
        self.rect = pygame.rect.FRect()
        
        self.healthbar = Healthbar(self)#init for healthbar
        if isinstance(self, Boss): #different healthbar for box
            self.healthbar.kill()
        self.image_offset = getattr(self, 'image_offset', (0, 0))
    #calculate stat for each time init
    def updstat(self):
        self.maxhp = self.raw_hp + self.level * self.hp_multiplier
        self.baseatk = self.raw_atk + self.level * self.atk_multiplier
        self.basedef = self.raw_def + self.level * self.def_multiplier
        
        self.hp = self.maxhp
        self.atk = self.baseatk
        self.def_ = self.basedef
        self.spd = self.basespd
    #wall collision logic
    def collision(self, dir_type, dir):
        for group in (self.game.collision_sprites, self.game.animated_tiles):
            for sprite in group:
                if sprite.rect.colliderect(self.rect):
                    if dir_type == 'horizontal':
                        if dir.x > 0: self.rect.right = sprite.rect.left
                        if dir.x < 0: self.rect.left = sprite.rect.right
                    else:
                        if dir.y < 0: self.rect.top = sprite.rect.bottom
                        if dir.y > 0: self.rect.bottom = sprite.rect.top
    #take damage logic
    def take_damage(self, dmg, pen = 0, type="normal"):
        if not self.alive():
            return
        
        if dmg < 0:
            dmg = 0    
    
        delta = dmg / (1 + 0.01 * self.def_ * (1 - pen))
        
        if hasattr(self, "invulnerable") and self.hp - delta < self.maxhp * self.invulnerable:
            delta = self.hp - self.invulnerable * self.maxhp
            
        if hasattr(self, "invulnerable") and delta == 0:
            Flyout_number(self.rect.center, "immune", (40, 40, 160), self.game, font_size=32)
            return
        
        self.hp -= delta
        
        if self.hp <= 0:
            self.death()
        
        # Flyout
        
        if delta < 0.5:
            return
        
        if type == "normal":
            Flyout_number(self.rect.center, int(delta), (255, 50, 50), self.game)
        
        if type == "poison":
            Flyout_number(self.rect.center, int(delta), (50, 195, 50), self.game, font_size=18)
        
        if type == "burning":
            Flyout_number(self.rect.center, int(delta), (255, 165, 50), self.game, font_size=18)
        
    def heal(self, healing, type="normal"):
        if not self.alive():
            return
        
        if type == "normal":
            Flyout_number(self.rect.center, "+" + str(int(healing)), (100, 255, 100), self.game)
        elif type == "overtime":
            Flyout_number(self.rect.center, "+" + str(int(healing)), (100, 255, 100), self.game, font_size=18)
        
        if isinstance(self, Boss) and self.phase == 2:
            self.hp = min(self.hp + healing, self.maxhp / 2)
        else:
            self.hp = min(self.hp + healing, self.maxhp)
    #death effect
    def death(self):
        self.kill()
    #moving logic for entity in general
    def move(self, dt):
        if self.meditating or self.stunned or self.rooted:
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        if not self.cross_wall:
            self.collision('horizontal', self.direction)

        self.rect.y += self.direction.y * self.spd * dt
        if not self.cross_wall:
            self.collision('vertical', self.direction)
        
        self.image_rect.center = (pygame.math.Vector2(self.rect.center) + self.image_offset)
    
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

        self.image_rect.center = (pygame.math.Vector2(self.rect.center) + self.image_offset)
    
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
        self.skills = {}
        
        # State
        self.frame_index = 0
        self.states=['Walking', 'Attacking']
        self.state='Walking'

        self.direction = pygame.Vector2(0, 0)
        
        #load image
        self.frames=game.enemy_frames[self.name]
        
        # image
        self.image = self.frames['Walking'][0]
        
        # rect
        self.rect = self.image.get_frect(center=pos)
        self.image_rect = self.rect.copy()

        self.image_rect.center = (pygame.math.Vector2(self.rect.center) + self.image_offset)
        #Tracking
        self.tracking = True
        self.tracker=Tracking(self.game,self,self.game.player)
        #Line of sight
        self.last_known_player_pos = pygame.Vector2(self.player.rect.center)
        self.has_direct_los = False
        #path finding if not have los
        self.path_vector_timer = 500  # ms
        self.path_vector_elapsed = 0
        self.cached_path_vector = pygame.Vector2()
        self.path = []
        self.path_index = 0
        self.cached_path_vector = pygame.Vector2()
    def has_line_of_sight(self):
        start = pygame.Vector2(self.rect.center)
        end = pygame.Vector2(self.player.rect.center)
        delta = end - start
        distance = delta.length()

        if distance == 0:
            return True

        direction = delta.normalize()
        steps = int(distance // 32)  # step every 32 pixels

        for i in range(steps + 1):  # +1 to include final check
            check_pos = start + direction * (i * 32)

            # 32x32 block centered at this sample point
            block_rect = pygame.Rect(0, 0, 32, 32)
            block_rect.center = check_pos

            for sprite in self.game.collision_sprites:
                if sprite.rect.colliderect(block_rect):
                    return False  # blocked by obstacle

        return True  # all clear
    def animate(self, dt):
        self.frame_index += self.animation_spd * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        if hasattr(self, 'asymmetry') and self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def death(self):
        if self.alive():
            self.game.spawn_numb -= 1
            Aninmated_Object(self.rect.center,'Grave2',self.game.all_sprites, self.game)
        super().death()

    def cal_dis(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.distance_vector = player_pos - enemy_pos
        self.facing_dir = self.distance_vector.normalize() if self.distance_vector else self.distance_vector
        #  Direct line of sight to player
        if self.has_line_of_sight():
            self.has_direct_los = True
            self.last_known_player_pos = player_pos
            self.path = []
            self.path_index = 0

            if self.distance_vector.length_squared() > 0:
                self.direction = self.distance_vector.normalize()

            else:
                self.direction = pygame.Vector2()
            return

        # No line of sight
        if self.has_direct_los:
            # Move toward last seen position
            to_last_known = self.last_known_player_pos - enemy_pos
            if to_last_known.length() > 4:
                self.direction = to_last_known.normalize()

                return
            else:
                # Reached last known pos
                self.has_direct_los = False

        # Use pathfinding if no LOS or reached last known pos
        self.path_vector_elapsed += dt * 1000
        if self.path_vector_elapsed >= self.path_vector_timer:
            self.path_vector_elapsed = 0
            self.path = self.tracker.get_path()
            self.path_index = 1  # skip current tile

        if self.path and self.path_index < len(self.path):
            target_cell = self.path[self.path_index]
            target_pos = pygame.Vector2(
                (target_cell[0] + 0.5) * self.tracker.cell_size,
                (target_cell[1] + 0.5) * self.tracker.cell_size
            )
            to_target = target_pos - enemy_pos

            if to_target.length() < 4:
                self.path_index += 1  # reached this tile
            elif to_target.length_squared() > 0:
                self.direction = to_target.normalize()

                return

        # No direction fallback
        self.direction = pygame.Vector2()
    def move_enemy(self,dt):
        # update the rect position + collision
        if self.forced_moving:
            self.forced_move(self.mode['dir'], dt)
            return
        
        if self.channeling or self.stunned or self.forced_moving or self.rooted:
            return
        
        distance = self.distance_vector.length()
        if distance <= self.keep_range and self.has_line_of_sight() :
            return
        
        self.rect.x += self.direction.x * self.spd * dt
        if not self.cross_wall:
            self.collision('horizontal', self.direction)
        self.enemy_collision('horizontal',dt)
        self.rect.y += self.direction.y * self.spd * dt
        
        if not self.cross_wall:
            self.collision('vertical', self.direction)

        self.image_rect.center = (pygame.math.Vector2(self.rect.center) + self.image_offset)
        
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
            self.cal_dis(dt)
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
        
        pygame.mixer.music.fadeout(2000)
        
        self.is_boss = True
        
        # Boss specific attributes
        self.phase = 1
        self.phase_change_hp = 0.5 * self.maxhp  # Change phase at 50% HP
        self.special_skills = []    # List of special skills for the boss

    def update(self, dt):
        super().update(dt)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join("audio", "BGM", f"{self.name}.wav"))
            pygame.mixer.music.play(loops=-1)
            
        if self.hp <= self.phase_change_hp and self.phase == 1:
            self.phase = 2
            self.change_phase()

    def change_phase(self):
        # Logic to change the boss's behavior or appearance when changing phases
        pass

    def death(self):
        super().death()
        pygame.mixer.music.fadeout(1000)
        Delay(1100, lambda: setattr(self.game, "current_BGM", None), self.game)