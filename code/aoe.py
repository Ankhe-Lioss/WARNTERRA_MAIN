from setting import *
from status import *
from helper import Delay

class Area_of_effect(pygame.sprite.Sprite):
    def __init__(self,pos,game,user_atk):
        super().__init__(game.all_sprites,game.aoe_sprites)
        self.user_atk=user_atk
        self.game = game

        #load stat
        self.scale = aoe_stat[self.name][0]
        self.frame_number = aoe_stat[self.name][1]
        self.lifetime = aoe_stat[self.name][2]
        #graphic loading

        self.frame_index = 0
        self.frames = self.game.aoe_frames[self.name]
        self.load_sound()
        if hasattr(self, 'sound'):
            self.sound.play()
        self.animation_speed = self.frame_number/self.lifetime*1000
        self.image = self.frames[0]
        self.image_rect = self.image.get_frect(center=pos)
        self.rect = self.image.get_frect(center=pos)
        

    def load_sound(self):
        if os.path.exists(os.path.join("audio", "aoe", f"{self.name}.ogg")):
            self.sound = pygame.mixer.Sound(os.path.join("audio", "aoe", f"{self.name}.ogg"))
            
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
    def aoe_collision(self):
        dmg = self.scale * self.user_atk

        # Initialize a hit tracker if it doesn't exist yet
        if not hasattr(self, 'hit_enemies'):
            self.hit_enemies = set()

        # Check for collisions
        collision_sprites = pygame.sprite.spritecollide(self, self.enemy_sprites, False)
        if collision_sprites:
            for sprite in collision_sprites:
                if sprite not in self.hit_enemies:
                    sprite.take_damage(dmg)
                    self.hit_enemies.add(sprite)
                    self.apply(sprite)

    def update(self, dt):
        self.animate(dt)
        self.aoe_collision()
        self.lifetime-=1000*dt
        if self.lifetime <= 0:
            self.kill()
            
    def apply(self, target):
        pass
            
class Poro_Stomp(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name='Poro_Stomp'
        super().__init__(pos,game,user_atk)
        
class Chogath_Rupture(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name='Chogath_Rupture'
        super().__init__(pos,game,user_atk)

    def apply(self, target):
        Stunned(1000, self.game, target)
        
class Veigar_Darkmatter(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name='Veigar_Darkmatter'
        super().__init__(pos,game,user_atk)

class Bow_explosion(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos,game,user_atk)
    
    def apply(self, target):
        Slowed(5000, 0.9, self.game, target)

class Soraka_star(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.player_sprites
        self.name=self.__class__.__name__
        super().__init__(pos,game,user_atk)

class Bazooka_pe(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos,game,user_atk)

class Bazooka_q(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos,game,user_atk)

class Bazooka_e(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos,game,user_atk)

    def apply(self, target):
        Burning(5000, apply_scale[self.name] * self.user_atk, self.game, target)

class Barrel_Explode(Area_of_effect):
    def __init__(self, pos,game,user_atk=0):
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_sprites.add(game.player_sprites, game.enemy_sprites)
        self.name='Barrel_Explode'
        super().__init__(pos,game,user_atk)

    def apply(self, target):
        Burning(2000, apply_scale[self.name][0] * target.maxhp if not hasattr(target, 'is_boss') else apply_scale[self.name][1] * target.maxhp, self.game, target)

class Calibrum_ult(Area_of_effect):
    def __init__(self, pos,game,user_atk):
        self.enemy_sprites=game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos,game,user_atk)
    
    def apply(self, target):
        Delay(1000, lambda : (Calibrum_mark(5000, self.game, target)), self.game)
        Delay(1000, lambda : (self.game.projectiles_audio["Calibrum_primary"].play()), self.game)

class Infernum_ult(Area_of_effect):
    def __init__(self, pos, game,user_atk):
        self.enemy_sprites = game.enemy_sprites
        self.name = self.__class__.__name__
        super().__init__(pos, game, user_atk)
    
    def apply(self, target):
        from player_projectiles import Infernum_burgeon
        Delay(1000, lambda : (Infernum_burgeon(target.rect.center, self.game, target)), self.game)
        