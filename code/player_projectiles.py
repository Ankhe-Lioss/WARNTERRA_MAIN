from projectiles import *
from status import *
from aoe import *
from helper import *

class Gauntlet_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-20, -20)

class Gauntlet_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.target, False)
        if collision_sprites:
            
            self.game.player.weap.q_skill.remaining -= 2000
            self.game.player.weap.e_skill.remaining -= 2000
            
            for sprite in collision_sprites:
                sprite.take_damage(self.dmg)
                self.play_sound()
                self.kill()
                break

class Gauntlet_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet SkillR"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.wall_piercing = True
        self.e_piercing = True
    
    def apply(self, target):
        Slowed(2000, 0.75, self.game, target)

class Bow_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-43, -43)
    def apply(self, target):
        Slowed(500, 0.2, self.game, target)

class Bow_primary_enhanced(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def apply(self, target):
        Slowed(500, 0.3, self.game, target)

class Bow_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillQ"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-33, -33)
    def apply(self, target):
        Slowed(1000, 0.6, self.game, target)

class Bow_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillE"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.wall_piercing = True
    
    def apply(self, target):
        Stunned(3000, self.game, target)
        Bow_explosion(self.rect.center, self.game, self.game.player.atk)

class Bazooka_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bazooka Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)

class Bazooka_primary_enhanced(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bazooka Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def kill(self):
        Bazooka_pe(self.rect.center, self.game, self.game.player.atk)
        super().kill()

class Bazooka_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bazooka SkillQ"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def kill(self):
        Bazooka_q(self.rect.center, self.game, self.game.player.atk)
        super().kill()

class Bazooka_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bazooka SkillE"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)

        # image for rotozoom
        
        self.target_sprite = self.find_nearest_enemy()

        if self.target_sprite:     
            self.tracker = Tracking(game, self, self.target_sprite)
            self.path = self.tracker.get_path()
            self.path_index = 1
        else:
            self.tracker = None
            self.path = []
            self.path_index = 0
        self.tracking = True
        
        m = min(self.rect.w, self.rect.h)
        
        self.rect.inflate_ip(-m + 10, -m + 10)

    def find_nearest_enemy(self):
        enemies = [e for e in self.game.enemy_sprites]
        if not enemies:
            return None
        my_pos = pygame.Vector2(self.rect.center)
        return min(enemies, key=lambda e: (pygame.Vector2(e.rect.center) - my_pos).length())

    def update(self, dt):
        
        if self.tracking and self.target_sprite and self.target_sprite.alive(): # Follow
            
            if self.path_index >= len(self.path):
                self.path = self.tracker.get_path()
                self.path_index = 1
                
            if self.path and self.path_index < len(self.path):
                next_cell = self.path[self.path_index]
                next_pos = (next_cell[0] * self.tracker.cell_size + self.tracker.cell_size // 2,
                            next_cell[1] * self.tracker.cell_size + self.tracker.cell_size // 2)
                move_vec = pygame.Vector2(next_pos) - pygame.Vector2(self.rect.center)
                
                # If the target moved too far, update the direction, else only update the path
                if move_vec.length() < 5:
                    self.path_index += 1
                else:
                    self.direction = move_vec.normalize()
            
            # ROTATE ERHIUADIFUHSIUDHISUAIHSDIAHDUASHDIASDHAIUSDHIASHDIUSHIUD
            if self.direction.length_squared() > 0:
                angle = -self.direction.angle_to(pygame.Vector2(1, 0))
                self.image = pygame.transform.rotozoom(self.image, -self.angle, 1)
                self.image = pygame.transform.rotozoom(self.image, angle, 1)
                self.image_rect = self.image.get_rect(center=self.rect.center)
        else:
            self.tracking = False  # Stop tracking if target is gone

        # Move
        self.rect.center += self.direction * self.spd * dt
        self.image_rect.center = self.rect.center

        # Other update (super() after subtracts)
        self._animate(dt)
        self.collision()
        self.bullet_collision()
        
        
        
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill()
        
    
    def kill(self):
        Bazooka_e(self.rect.center, self.game, self.game.player.atk)
        super().kill()