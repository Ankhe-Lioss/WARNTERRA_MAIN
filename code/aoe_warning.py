from aoe import *
class Spawn_rupture(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game,user_atk):
        super().__init__(groups)
        #pass to aoe
        self.game=game
        self.groups=groups
        self.pos=pos
        self.user_atk=user_atk

        #
        self.frame_index = 0
        self.frames=[]
        self.load_frame()
        self.animation_speed = 6
        self.lifetime=500
        self.spawn_time=pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=pos)

    def load_frame(self):
        for i in range(3):
            surf=pygame.image.load(os.path.join('images', 'enviroment','spawn_rupture', f'{i}.png')).convert_alpha()
            self.frames.append(surf)

    def spawn(self):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
            Chogath_Rupture(self.pos,self.groups,self.game,self.user_atk)
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    def update(self, dt):
        self.animate(dt)
        self.spawn()
