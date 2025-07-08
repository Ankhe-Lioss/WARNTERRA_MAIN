from aoe import *
from status import *

Spawn_aoe_dict={  #aoe skill=[frame_number,life_time]d
    'Spawn_rupture':(3, 500),
    'Spawn_darkmatter':(6, 1000),
    'Spawn_Soraka_star' : (6, 1000),
    'Spawn_Soraka_cc' : (12, 2000),
    'Dust_trace':(8,400)
}
#the sprite that end when it reach its life time
class Spawn_aoe(pygame.sprite.Sprite):
    def __init__(self, pos, game, user_atk=0):
        super().__init__(game.all_sprites)
        #pass to aoe
        self.game=game
        self.pos=pos
        self.user_atk=user_atk
        #pass from dic
        self.stat=Spawn_aoe_dict[self.name]
        self.frame_number=self.stat[0]
        self.lifetime=self.stat[1]
        self.frame_index = 0
        #loading graphics
        self.frames = self.game.aoe_warning_frames[self.name]
        self.animation_speed = 6
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=pos)
        #radius if check if it a circle
        self.radius = self.rect.width / 2 + 20
        self.image_rect = self.image.get_frect(center=pos)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    def update(self, dt):
        self.lifetime -= dt*1000
        if self.lifetime <= 0:
            self.kill()
            self.spawn()
        self.animate(dt)
        
class Spawn_rupture(Spawn_aoe):
    def __init__(self, pos, game, user_atk):
        self.name='Spawn_rupture'
        super().__init__( pos, game, user_atk)
    def spawn(self):
        Chogath_Rupture(self.pos, self.game, self.user_atk)
            
class Spawn_darkmatter(Spawn_aoe):
    def __init__(self, pos, game, user_atk):
        self.name='Spawn_darkmatter'
        super().__init__( pos, game, user_atk)
    def spawn(self):
        Veigar_Darkmatter(self.pos, self.game, self.user_atk)

class Spawn_Soraka_star(Spawn_aoe):
    def __init__(self, pos, game, user_atk):
        self.name=self.__class__.__name__
        super().__init__( pos, game, user_atk)
    def spawn(self):
        Soraka_star(self.pos, self.game, self.user_atk)

class Spawn_Soraka_cc(Spawn_aoe):
    def __init__(self, pos, game, user):
        self.name=self.__class__.__name__
        self.user = user
        super().__init__( pos, game, user.atk)
        
    def update(self, dt):
        super().update(dt)
        if (pygame.Vector2(self.game.player.rect.center) - pygame.Vector2(self.pos)).length() <= self.radius:
            Silenced(100, self.game, self.game.player)
        
        
        # CHECK
        offset = self.game.all_sprites.offset
        screen_pos = pygame.Vector2(self.rect.center) + offset
        pygame.draw.circle(pygame.display.get_surface(), 'aqua', screen_pos, self.radius, width=5)
    
    def spawn(self):
        if (pygame.Vector2(self.game.player.rect.center) - pygame.Vector2(self.pos)).length() <= self.radius and self.user.phase == 2:
            Rooted(2000, self.game, self.game.player)
class Dust_trace(Spawn_aoe):
    def __init__(self, pos, game):
        self.name='Dust_trace'
        super().__init__(pos, game)
        self.type='floor'
    def spawn(self):
        pass