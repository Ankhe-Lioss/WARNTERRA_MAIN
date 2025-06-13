from setting import *
from status import *

class Area_of_effect(pygame.sprite.Sprite):
    def __init__(self,pos,groups,game,user_atk):
        super().__init__(groups)
        self.user_atk=user_atk
        self.game = game

        #load stat
        self.scale=Aoe_stat[self.name][0]
        self.frame_number=Aoe_stat[self.name][1]
        self.lifetime = Aoe_stat[self.name][2]
        #graphic loading

        self.frame_index = 0
        self.frames = []
        self.load_frame()
        self.animation_speed = self.frame_number/self.lifetime*1000
        self.spawn_time = pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=pos)
        
    def load_frame(self):
        for i in range(self.frame_number):
            surf=pygame.image.load(os.path.join('images', 'aoe',f'{self.name}', f'{i}.png')).convert_alpha()
            self.frames.append(surf)
            
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
    def aoe_collision(self):
        dmg = self.scale * self.user_atk

        # Initialize a hit tracker if it doesn't exist yet
        if not hasattr(self, 'hit_enemies'):
            self.hit_enemies = set()

        # Check for collisions
        collision_sprites = pygame.sprite.spritecollide(self, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                if sprite not in self.hit_enemies:
                    sprite.take_damage(dmg)
                    self.hit_enemies.add(sprite)
                    self.apply(sprite)

    def update(self, dt):
        self.animate(dt)
        self.aoe_collision()
        if pygame.time.get_ticks()-self.spawn_time>=self.lifetime:
            self.kill()
            
    def apply(self, target):
        pass
            
class Poro_Stomp(Area_of_effect):
    def __init__(self, pos, groups, game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name='Poro_Stomp'
        super().__init__(pos,groups,game,user_atk)
        
class Chogath_Rupture(Area_of_effect):
    def __init__(self, pos, groups, game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name='Chogath_Rupture'
        super().__init__(pos,groups,game,user_atk)

    def apply(self, target):
        target.status.add(Stunned(1000, self.game, target))