from setting import *
from sprites import *
class Projectiles(pygame.sprite.Sprite):
    def __init__(self, target, pos, direction, groups, game):
        # Initializing
        super().__init__(groups, game.all_sprites)
        self.game = game
        self.target = target
        
        # Movement
        self.direction = direction
        self.angle = degrees(atan2(self.direction.x, self.direction.y)) - 90
        
        # Hitbox

        self.lifetime = 5000
        
        # Loading appearance
        self.animation_spd = 4
        self.frames = []
        self._load_images()
        self.frame_id = 0
        self.image = self.frames[self.frame_id]
        
        # Rect
        self.image_rect = self.image.get_frect(center=pos)
        self.rect = self.image.get_frect(center=pos)
        
        # Audio
        if os.path.exists(os.path.join('audio', 'projectiles', f'{self.name}.ogg')):
            self.sound = pygame.mixer.Sound(os.path.join('audio', 'projectiles', f'{self.name}.ogg'))

    def _load_images(self):
        folder, folder1 = self.source.split(" ")
        # Use preloaded frames
        base_frames = self.game.projectile_frames.get(folder, {}).get(folder1, [])
        self.frames = []
        for surf in base_frames:
            # Rotate each frame as needed
            rotated = pygame.transform.rotozoom(surf, self.angle, 1)
            self.frames.append(rotated)
    
    def _animate(self, dt):
        self.frame_id += self.animation_spd * dt
        self.image = self.frames[int(self.frame_id) % len(self.frames)]
    
    def collision(self):


        collisions = pygame.sprite.spritecollide(self, self.game.collision_sprites, False)

        for sprite in collisions:
            if isinstance(sprite, Explosive_Barrel):
                if sprite.state == 'idle':
                    sprite.state = 'warning'
                    sprite.warning_timer = 0
        if hasattr(self,'wall_piercing') and self.wall_piercing:
            return
        if collisions:
            self.kill()
            return
    
    def update(self, dt):
        self._animate(dt)
        self.rect.center += self.direction * self.spd * dt
        self.image_rect.center = self.rect.center
        self.collision()
        self.bullet_collision()
        
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill()
    
    def apply(self, target):
        pass
    def play_sound(self):
        if hasattr(self, 'sound'):
            self.sound.play()
        
    def collide(self, sprite):
        self.play_sound()
        self.apply(sprite)
        sprite.take_damage(self.dmg)
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.target, False)
        if collision_sprites:
            for sprite in collision_sprites:
                
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

class Player_projectiles(Projectiles):
    def __init__(self, pos, direction, game):
        # Init
        super().__init__(game.enemy_sprites, pos, direction, game.player_projectiles, game)
        
        # Calcu
        self.scale, self.spd = player_projectiles[self.name]
        self.dmg = self.scale * self.game.player.atk                    
             
class Enemy_projectiles(Projectiles):
    def __init__(self, user, pos, direction, game):
        # Init
        self.user = user
        super().__init__(game.player_sprites, pos, direction, game.enemy_projectiles, game)
        
        # Calcu
        self.scale, self.spd = enemy_projectiles[self.name]
        self.dmg = self.scale * self.user.atk

