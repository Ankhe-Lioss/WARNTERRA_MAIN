from aoe import *
from status import *

Spawn_aoe_dict={  #aoe skill=[frame_number,life_time]d
    'Spawn_rupture':(3, 500),
    'Spawn_darkmatter':(6, 1000),
    'Spawn_Soraka_star' : (6, 1000),
    'Spawn_Soraka_cc' : (6, 2000)
}
class Spawn_aoe(pygame.sprite.Sprite):
    def __init__(self, pos, game, user_atk):
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
        self.frames=[]
        self.load_frame()
        self.animation_speed = 6
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=pos)
        self.radius = float(self.rect.top) + 20
        self.image_rect = self.image.get_frect(center=pos)

    def load_frame(self):
        for i in range(self.frame_number):
            surf=pygame.image.load(os.path.join('images', 'enviroment',f'{self.name}', f'{i}.png')).convert_alpha()
            self.frames.append(surf)

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
            self.game.player.status.add(Silenced(dt * 1000, self.game, self.game.player))
    
    def spawn(self):
        if (pygame.Vector2(self.game.player.rect.center) - pygame.Vector2(self.pos)).length() <= self.radius and self.user.phase == 2:
            self.game.player.status.add(Rooted(2000, self.game, self.game.player))
            