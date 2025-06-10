from setting import *

class Surf:
    def __init__(self, surf = pygame.surface.Surface((1, 1)), rect = pygame.rect.FRect()):
        self.surf = surf
        self.rect = rect

class stat_ui(pygame.sprite.Sprite):
    def __init__(self, player, game):
        super().__init__(game.all_sprites)
        self.is_stat_ui = True
        
        # Stats
        self.maxhp, self.hp = player.maxhp, player.hp
        self.player = player
        self.game = game
        
        # Image
        self.surfaces = []
    
    def update(self, dt):
        # Update stats, init surfaces
        self.surfaces = []
        self.maxhp, self.hp = self.player.maxhp, self.player.hp
        
        self.fullhp = Surf()
        self.fullhp.surf = pygame.Surface((50, 10), pygame.SRCALPHA)
        self.fullhp.surf.fill('grey20')
        self.fullhp.rect = self.fullhp.surf.get_frect(center=self.player.rect.center + pygame.Vector2(y=-40))
        
        self.curhp = Surf()
        self.curhp.surf = pygame.Surface((50 * self.hp / self.maxhp, 10), pygame.SRCALPHA)
        self.curhp.surf.fill('green')
        self.curhp.rect = self.fullhp.rect.copy()
        self.curhp.rect.topleft = self.fullhp.rect.topleft
        
        self.surfaces = [self.fullhp, self.curhp]