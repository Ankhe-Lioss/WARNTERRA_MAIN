from setting import *

class Ground(pygame.sprite.Sprite):
    
    """ Background map """
    
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.ground = True
        
class CollisionSprite(pygame.sprite.Sprite):
    
    """ Objects and walls """
    
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image_rect = self.image.get_rect(topleft=pos)
        self.rect = self.image.get_frect(topleft=pos)
        
        
class Check_in(pygame.sprite.Sprite):
    def __init__(self, pos,game):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = pygame.image.load(os.path.join('images','enviroment','check_in','0.png'))
        self.rect = self.image.get_rect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.visible = True
        
    def update(self, dt):
        if pygame.sprite.spritecollide(self, self.game.player_sprites,False):
            self.kill()
            self.game.spawn_numb -= 1



class Door(pygame.sprite.Sprite):
    """ Objects and walls """

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image_rect = self.image.get_rect(topleft=pos)
        self.rect = self.image.get_frect(topleft=pos)

