from setting import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, game):
        
        # Initializing
        super().__init__(groups)
        
        # Setting group
        self.enemy_sprites = game.enemy_sprites
        self.collision_sprites = game.collision_sprites
        
        # Movement
        self.direction = direction
        self.speed = 1200 #undef
        
        # Hitbox
        self.rect = self.image.get_frect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000
        
        # Loading appearance
        self.load_images()
        self.rotate()
        self.image = self.bullet_surf

        
        
    def load_images(self):
        folder,file_name=(self.name).split('_')
        self.bullet_surf = pygame.image.load(os.path.join('images', 'projectiles', f'{folder}',f'{file_name}.png')).convert_alpha()
        
    def rotate(self):
        angle = degrees(atan2(self.direction.x, self.direction.y)) + 180
        self.bullet_surf= pygame.transform.rotozoom(self.bullet_surf, angle, 1)
        
    def bullet_collision(self):
        collision_sprites=pygame.sprite.spritecollide(self,self.enemy_sprites,False,pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                sprite.destroy()
                self.kill()
    def collision(self):
        if pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_mask):
            self.kill()
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.collision()
        self.bullet_collision()
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        
class Gauntlet_Primary(Bullet):
    def __init__(self, pos, direction, groups,game):
        self.name='Gauntlet_Primary'
        super().__init__(pos,direction,groups,game)