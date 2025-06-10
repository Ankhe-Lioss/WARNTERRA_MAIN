from setting import *

class Projectiles(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, game):
        # Initializing
        super().__init__(groups)
        self.game = game
        
        # Movement
        self.direction = direction
        self.angle = degrees(atan2(self.direction.x, self.direction.y)) - 90
        
        # Hitbox
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000
        
        # Loading appearance
        self.animation_spd = 4
        self.frames = []
        self._load_images()
        self.frame_id = 0
        self.image = self.frames[self.frame_id]
        
        self.rect = self.image.get_frect(center=pos)
    
    def _load_images(self):
        folder, folder1 = self.source.split(" ")

        for i in range(4):
            surf = pygame.image.load(os.path.join('images', 'projectiles', f'{folder}',f'{folder1}',f'{i}.png')).convert_alpha()
            surf = pygame.transform.rotozoom(surf, self.angle,1)
            self.frames.append(surf)
        
    def _animate(self, dt):
        self.frame_id += self.animation_spd * dt
        self.image = self.frames[int(self.frame_id) % len(self.frames)]
    
    def collision(self):
        if hasattr(self,'piercing') and self.piercing:
            return
        if pygame.sprite.spritecollide(self, self.game.collision_sprites, False):
            self.kill()
    
    def update(self, dt):
        self._animate(dt)
        self.rect.center += self.direction * self.spd * dt
        self.collision()
        self.bullet_collision()

class Player_projectiles(Projectiles):
    def __init__(self, pos, direction, groups, game):
        # Init
        super().__init__(pos, direction, groups, game)
        
        # Calcu
        self.scale, self.spd = player_projectiles[self.name]
        self.dmg = self.scale * self.game.player.atk
        
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                
                if not hasattr(self, "piercing") or not self.piercing:
                    sprite.take_damage(self.dmg)
                    self.kill()
                else:
                    if not hasattr(sprite, "get_shot"):
                        sprite.take_damage(self.dmg)
                        sprite.get_shot = [self]
                    else:
                        this_sprite_got_shot_by_this_proj = False
                        for proj in sprite.get_shot:
                            if proj is self:
                                this_sprite_got_shot_by_this_proj = True
                                
                        if not this_sprite_got_shot_by_this_proj:
                            sprite.take_damage(self.dmg)
                            sprite.get_shot.append(self)
                                
                        
             
class Enemy_projectiles(Projectiles):
    def __init__(self, pos, direction, groups, game):
        # Init
        super().__init__(pos, direction, groups, game)
        
        # Calcu
        self.scale, self.spd = enemy_projectiles[self.name]
        self.dmg = self.scale * self.game.player.atk
        
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.game.player_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                sprite.take_damage(self.dmg)
                self.kill()
