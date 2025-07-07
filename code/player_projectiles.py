from projectiles import *
from status import *
from aoe import *
from helper import *
import random

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
            self.game.player.weap.secondary.remaining = 0
            
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
        self.rect=self.rect.inflate(-60, -60)
        
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
        
        m = min(self.rect.w, self.rect.h)
        self.rect.inflate_ip(-m + 10, -m + 10)
    
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
        self.lifetime = 60000

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
            
            
        else:
            self.direction = pygame.Vector2(self.target_sprite.rect.center - self.rect.center).normalize()
            self.tracking = False  # Stop tracking if target is gone

        # Move
        self.rect.center += self.direction * self.spd * dt
        self.image_rect.center = self.rect.center

        # Other update (super() after subtracts)
        self._animate(dt)
        
        # ROTATE ERHIUADIFUHSIUDHISUAIHSDIAHDUASHDIASDHAIUSDHIASHDIUSHIUD
        if self.direction.length_squared() > 0 and self.tracking:
            angle = self.direction.angle_to(pygame.Vector2(1, 0))
            self.image = pygame.transform.rotozoom(self.image, -self.angle, 1)
            self.image = pygame.transform.rotozoom(self.image, angle, 1)
            self.image_rect = self.image.get_rect(center=self.rect.center)
        
        # Check collision
        self.collision()
        self.bullet_collision()
        
        
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill()
        
    
    def kill(self):
        Bazooka_e(self.rect.center, self.game, self.game.player.atk)
        super().kill()

def Infernum_wave(pos, dir, game, target):
    Infernum_ray(pos, dir.rotate(-15), game, target)
    Infernum_ray(pos, dir.rotate( -5), game, target)
    Infernum_ray(pos, dir.rotate( 5 ), game, target)
    Infernum_ray(pos, dir.rotate( 15), game, target)
    game.projectiles_audio["Infernum_beam"].play()

def Infernum_burgeon(pos, game, target):
    angle = random.randrange(0, 45)
    for i in range(0, 360, 45):
        Infernum_ray(pos, pygame.Vector2(1, 0).rotate(angle + i), game, target)
    game.projectiles_audio["Infernum_beam"].play()

class Calibrum_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Lunar_gun Left"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-20, -20)
    
    def apply(self, target):
        if hasattr(target, "calibrum_aura") and target.calibrum_aura is not None:
            target.calibrum_aura.cleanse()
                
            Infernum_wave(self.rect.center, self.direction, self.game, target)
            target.take_damage(apply_scale["Calibrum_mark"] * self.game.player.atk)
            Buff(1000, 0.3, 'spd', self.game, self.game.player)

class Infernum_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Lunar_gun Right"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-20, -20)
    
    def apply(self, target):
        Infernum_wave(self.rect.center, self.direction, self.game, target)
        
class Infernum_ray(Player_projectiles):
    def __init__(self, pos, direction, game, ignored_target):
        self.source = "Lunar_gun Right"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        
        self.e_piercing = True
        self.wall_piercing = True
        self.lifetime = 250
        self.ignored_target = ignored_target
        self.rect=self.rect.inflate(0, 0)
        
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.target, False)
        if collision_sprites:
            for sprite in collision_sprites:
                if sprite is self.ignored_target:
                    continue
                
                if not hasattr(self, "e_piercing") or not self.e_piercing:
                    self.collide(sprite)
                    self.kill()
                    break
                else:
                    if not hasattr(sprite, "get_shot"):
                        self.collide(sprite)
                        sprite.get_shot = [self]
                    else:
                        this_sprite_got_shot_by_this_proj = False
                        for proj in sprite.get_shot:
                            if proj is self:
                                this_sprite_got_shot_by_this_proj = True
                                
                        if not this_sprite_got_shot_by_this_proj:
                            self.collide(sprite)
                            sprite.get_shot.append(self)

class Calibrum_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Lunar_gun Q"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-20, -20)
    
    def apply(self, target):
        Calibrum_mark(5000, self.game, target)

class Infernum_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Lunar_gun Infernum_Q"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(0, 0)
        self.e_piercing = True
        self.wall_piercing = True
        self.lifetime = 250
    
    def apply(self, target):
        Delay(500, lambda : Calibrum_mark(3000, self.game, target), self.game)
        Delay(500, lambda : (self.game.projectiles_audio["Calibrum_primary"].play()), self.game)

class Lunar_ult(Player_projectiles):
    def __init__(self, pos, direction, game, gun_type):
        self.source = "Lunar_gun E"
        self.name = self.__class__.__name__
        
        self.gun_type = gun_type
        super().__init__(pos, direction, game)
        self.wall_piercing = True
        
        self.rect.inflate_ip(-10, -10)
    
    def apply(self, target):
        if self.gun_type == "Calibrum":
            Calibrum_ult(self.rect.center, self.game, self.game.player.atk)
        else:
            Infernum_ult(self.rect.center, self.game, self.game.player.atk)