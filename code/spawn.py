from setting import *
from enemies import *
from sprites import *
def spawn_poro(pos,game):
    Poro(pos, game)
def spawn_meele(pos,game):
    Meele(pos, game)
def spawn_karthus(pos,game):
    Karthus(pos, game)
def Spawm_chogath(pos,game):
    Chogath(pos, game)
def spawn_animation(pos,game,enemy_name):
    spawn_animation(pos,(game.all_sprites),game,enemy_name)

class spawn_animation(pygame.sprite.Sprite):
    def __init__(self, pos, game, enemy_name):
        super().__init__(game.all_sprites)
        self.game=game
        self.frame_index = 0
        self.frames=[]
        self.load_frame()
        self.enemy_name=enemy_name
        self.animation_speed = 10
        self.lifetime=1500
        self.spawn_time=pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)

    def load_frame(self):
        for i in range(15):
            surf=pygame.image.load(os.path.join('images', 'enviroment','enemy_spawn_animation', f'{i}.png')).convert_alpha()
            self.frames.append(surf)
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
    def spawn(self):
        if pygame.time.get_ticks()-self.spawn_time>=self.lifetime:
            self.kill()
            if self.enemy_name=='Poro':
                spawn_poro((self.rect.center),self.game)
            if self.enemy_name=='Meele':
                spawn_meele((self.rect.center),self.game)
            if self.enemy_name=='Karthus':
                spawn_karthus((self.rect.center),self.game)
            if self.enemy_name=='Chogath':
                Spawm_chogath((self.rect.center),self.game)
            if self.enemy_name=='Check_in':
                Check_in((self.rect.center),self.game)
    def update(self, dt):
        self.animate(dt)
        self.spawn()
