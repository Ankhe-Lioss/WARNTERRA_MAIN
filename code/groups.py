import pygame.math

from setting import *

SHOW_HITBOX = False
Show_image=False
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, player):
        self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
        self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)
        ground_sprites = []
        floor_sprites = []
        object_sprites = []
        top_sprites = []

        for sprite in self:
            if not hasattr(sprite, 'get_draw') or sprite.get_draw==False:
                continue
            if hasattr(sprite, 'visible') and sprite.visible == False:
                continue
            if not hasattr(sprite, 'image_rect') or sprite.image_rect is None:
                continue

            sprite_type = getattr(sprite, 'type', None)
            if sprite_type == 'ground':
                ground_sprites.append(sprite)
            elif sprite_type == 'floor':
                floor_sprites.append(sprite)
            elif sprite_type == 'top':
                top_sprites.append(sprite)
            elif sprite_type not in ['ground', 'floor', 'top', 'door'] and sprite_type !="weap":
                object_sprites.append(sprite)
            elif sprite_type is None:
                object_sprites.append(sprite)

        for layer in [ground_sprites, floor_sprites, object_sprites, top_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.image_rect.centery):
                if hasattr(sprite,"name") and   sprite.name=="Player" and hasattr(sprite, 'weap'):
                    self.display_surface.blit(sprite.weap.image, sprite.weap.image_rect.topleft + self.offset)
                self.display_surface.blit(sprite.image, sprite.image_rect.topleft + self.offset)

                if Show_image and not hasattr(sprite, 'type') :
                    image_rect_outline = sprite.image_rect.copy()
                    image_rect_outline.topleft += self.offset
                    pygame.draw.rect(self.display_surface, (255, 255, 100), image_rect_outline, 1)  # Light yellow
                if SHOW_HITBOX and not hasattr(sprite, 'type') and sprite.rect is not None:
                    if sprite.rect == None:
                        print(sprite.__class__.__name__, "has no rect attribute")
                    rect = sprite.rect.copy()
                    rect.topleft += self.offset
                    pygame.draw.rect(self.display_surface, 'red', rect, 1)
    def update(self, dt,player):
        for sprite in self.sprites():
            if not hasattr(sprite, 'image_rect') or sprite.image_rect is None:
                continue

            sprite_offset = pygame.math.Vector2(sprite.image_rect.center) - pygame.math.Vector2(player.rect.center)
            if sprite_offset.length_squared() > 4000*4000:  # or 1000, or whatever makes sense
                continue
            sprite.update(dt)
            sprite.get_draw = True if sprite_offset.length_squared() < 1000 * 1000 else False
