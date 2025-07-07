import pygame.image

from setting import *
#background that run on loop when open the menu
class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.frame_index = 0
        self.frames = []
        self.load_frame()
        self.image = self.frames[self.frame_index]
        self.animation_spd = 6

    def load_frame(self):
        for i in range(18):
            surf=pygame.image.load(os.path.join('images','enviroment','background',f'{i}.png'))
            self.frames.append(surf)
    def draw(self,dt,screen):
        self.frame_index += self.animation_spd * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        screen.blit(self.image,(0,0))