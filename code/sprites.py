from setting import *

class Ground(pygame.sprite.Sprite):
    
    """ Background map """
    
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image_rect = self.image.get_frect(topleft=pos)
        self.ground = True
        
class CollisionSprite(pygame.sprite.Sprite):
    
    """ Objects and walls """
    
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image_rect = self.image.get_frect(topleft=pos)
