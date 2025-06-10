from setting import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        statui_sprites = [sprite for sprite in self if hasattr(sprite, 'is_stat_ui')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') and not hasattr(sprite, 'is_stat_ui')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
        
        for sprite in statui_sprites:
            for surface in sprite.surfaces:
                self.display_surface.blit(surface.surf, surface.rect.topleft + self.offset)