from projectiles import *
from status import *

class Karthus_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Karthus Primary'
        self.wall_piercing = True
        super().__init__(user, direction, game)

class Veigar_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Primary'
        super().__init__(user, direction, game)
        self.rect.inflate(-50, -50)

class Veigar_Secondary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Secondary'
        super().__init__(user, direction, game)
        self.rect.inflate_ip(-30, -30)

class Veigar_Ult(Enemy_projectiles):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.source='Veigar Ult'
        super().__init__(user, pygame.Vector2(0, 0), game)
        self.rect = self.image_rect.inflate(-80, -80)
        self.wall_piercing = True
        self.lifetime = 20000
    
    def update(self, dt):
        # Track the player
        self.direction = pygame.Vector2(self.game.player.rect.center) - pygame.Vector2(self.rect.center)
        self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction
        super().update(dt)
    
    def collide(self, sprite):
        sprite.take_damage(sprite.maxhp * 0.5, pen=0.5, type="normal")
        self.play_sound()

class Lulu_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Lulu Primary'
        super().__init__(user, direction, game)
    
    def apply(self, target):
        target.status.add(Slowed(3000, 0.5, self.game, target))

class Veigar_Cage(pygame.sprite.Sprite):
    def __init__(self, center, outer_radius, inner_radius, game):
        super().__init__(game.all_sprites)
        self.game = game

        size = outer_radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw outer circle (ring)
        pygame.draw.circle(self.image, (120, 0, 255, 180), (outer_radius, outer_radius), outer_radius)
        # Cut out the inner circle (make it transparent)
        pygame.draw.circle(self.image, (0, 0, 0, 0), (outer_radius, outer_radius), inner_radius)
        self.rect = self.image.get_rect(center=center)
        self.image_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        player = self.game.player
        
        offset_x = int(player.rect.left - self.rect.left)
        offset_y = int(player.rect.top - self.rect.top)

        if self.mask.overlap(pygame.mask.from_surface(self.image), (offset_x, offset_y)):
            if not hasattr(player, "caged") or not player.caged:
                player.status.add(Stunned(3000, self.game, player))
                player.caged = True
        else:
            player.caged = False