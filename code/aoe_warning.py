from aoe import *
Spawn_aoe_dict={  #aoe skill=[frame_number,life_time]d
    'Spawn_rupture':(3, 500),
    'Spawn_darkmatter':(3, 1000)
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
