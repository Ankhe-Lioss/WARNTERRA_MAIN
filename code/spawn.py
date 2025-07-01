from setting import *
from enemies import *
from bosses import *
from sprites import *
    
enemy_classes = {
    'Poro': Poro,
    'Meele': Meele,
    'Karthus': Karthus,
    'Chogath': Chogath,
    'Check_in': Check_in,
    'Veigar': Veigar,
    'Lulu' : Lulu,
    'Nocturne' : Nocturne,
    'Maokai' : Maokai,
    'Soraka' : Soraka
}

def spawn_animation(pos,game,enemy_name):
    spawn_animation(pos,game,enemy_name)

class spawn_animation(pygame.sprite.Sprite):
    def __init__(self, pos, game, enemy_name):
        super().__init__(game.all_sprites)
        self.game=game
        self.frame_index = 0
        self.frames = self.game.spawn_frames
        self.enemy_name=enemy_name
        self.animation_speed = 10
        self.lifetime = 1500
        
        # Skip for check in
        if enemy_name == 'Check_in':
            self.lifetime = 0
            
        self.image = self.frames[0]
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_frect(topleft=pos)
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
    def spawn(self):
        if self.lifetime<=0:
            self.kill()

            if self.enemy_name in enemy_classes:
                enemy_class = enemy_classes[self.enemy_name]
                enemy_class(self.rect.center, self.game)

    def update(self, dt):
        self.lifetime -= dt*1000
        self.animate(dt)
        self.spawn()
