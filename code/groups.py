from setting import *

SHOW_HITBOX = False

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos.centerx - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos.centery - WINDOW_HEIGHT / 2)
        
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'type') and sprite.type == 'ground']
        floor_sprites = [sprite for sprite in self if hasattr(sprite, 'type') and sprite.type == 'floor']
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'type') or not sprite.type in ['ground', 'floor', 'top', 'collision', 'door']]
        top_sprites = [sprite for sprite in self if hasattr(sprite, 'type') and sprite.type == 'top']

        for layer in [ground_sprites, floor_sprites, object_sprites, top_sprites]:
            for sprite in sorted(layer, key=lambda sprite: (sprite.image_rect if hasattr(sprite, 'image_rect') else sprite.rect).y):
                if hasattr(sprite, 'visible') and sprite.visible==False:
                    continue
                self.display_surface.blit(sprite.image, sprite.image_rect.topleft + self.offset)
                if SHOW_HITBOX and not hasattr(sprite, 'type') and sprite.rect is not None:
                    """if sprite.rect == None:
                        print(sprite.__class__.__name__, "has no rect attribute")"""
                    rect = sprite.rect.copy()
                    rect.topleft += self.offset
                    pygame.draw.rect(self.display_surface, 'red', rect, 1)
             
        