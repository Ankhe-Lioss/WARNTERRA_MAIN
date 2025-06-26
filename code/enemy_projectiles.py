from projectiles import *
from status import *

class Karthus_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Karthus Primary'
        self.wall_piercing = True
        super().__init__(user, user.rect.center, direction, game)

class Veigar_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Primary'
        super().__init__(user, user.rect.center, direction, game)
        self.rect.inflate(-50, -50)

class Veigar_Secondary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Veigar Secondary'
        super().__init__(user, user.rect.center, direction, game)
        self.rect.inflate_ip(-30, -30)

class Veigar_Ult(Enemy_projectiles):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.source='Veigar Ult'
        super().__init__(user, user.rect.center, pygame.Vector2(0, 0), game)
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
        super().__init__(user, user.rect.center, direction, game)
    
    def apply(self, target):
        Slowed(3000, 0.5, self.game, target)

class Veigar_Cage(pygame.sprite.Sprite):
    def __init__(self, center, outer_radius, inner_radius, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.lifetime = 5000
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
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
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill()
        dist = (pygame.Vector2(player.rect.center) - pygame.Vector2(self.center)).length()

        if self.inner_radius - 20 <= dist and dist <= self.outer_radius + 20:
            if not hasattr(player, "caged") or not player.caged:
                Stunned(1500, self.game, player)
                player.caged = True
        else:
            player.caged = False

class Healing_Buff(Enemy_projectiles):
    def __init__(self, user, pos, game, skill):
        self.name = self.__class__.__name__
        self.source = "Other Healing_buff"
        super().__init__(user, pos, pygame.Vector2(), game)
        self.lifetime = 999999999
        self.used = False
        self.skill = skill
    
    def apply(self, target):
        Healing(2000, self.game.player.maxhp * 0.125, self.game, target)
        self.used = True
        
    def update(self, dt):
        super().update(dt)
        self.skill.remaining = self.skill.cooldown

class Speed_Buff(Enemy_projectiles):
    def __init__(self, user, pos, game, skill):
        self.name = self.__class__.__name__
        self.source = "Other Speed_buff"
        super().__init__(user, pos, pygame.Vector2(), game)
        self.lifetime = 999999999
        self.used = False
        self.skill = skill
    
    def apply(self, target):
        Buff(5000, 0.3, 'spd', self.game, target)
        self.used = True
    
    def update(self, dt):
        super().update(dt)
        self.skill.remaining = self.skill.cooldown


class Attack_Buff(Enemy_projectiles):
    def __init__(self, user, pos, game, skill):
        self.name = self.__class__.__name__
        self.source = "Other Attacking_buff"
        super().__init__(user, pos, pygame.Vector2(), game)
        self.lifetime = 999999999
        self.used = False
        self.skill = skill

    def apply(self, target):
        Buff(5000, 0.3, 'atk', self.game, target)
        self.used = True

    def update(self, dt):
        super().update(dt)
        self.skill.remaining = self.skill.cooldown

class Maokai_Primary(Enemy_projectiles):
    def __init__(self, user, direction, game):
        self.name = self.__class__.__name__
        self.source='Maokai Primary'
        self.wall_piercing = True
        super().__init__(user, user.rect.center, direction, game)
        self.lifetime = 250
    
    def apply(self, target):
        Slowed(1000, 0.6, self.game, target)