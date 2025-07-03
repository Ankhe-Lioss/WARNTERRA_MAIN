from projectiles import *
from status import *
from aoe import *

class Gauntlet_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-20, -20)

class Gauntlet_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.target, False)
        if collision_sprites:
            
            self.game.player.weap.q_skill.remaining -= 2000
            self.game.player.weap.e_skill.remaining -= 2000
            
            for sprite in collision_sprites:
                sprite.take_damage(self.dmg)
                self.play_sound()
                self.kill()
                break

class Gauntlet_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Gauntlet SkillR"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.wall_piercing = True
        self.e_piercing = True
    
    def apply(self, target):
        Slowed(2000, 0.75, self.game, target)

class Bow_primary(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Primary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-43, -43)
    def apply(self, target):
        Slowed(500, 0.2, self.game, target)

class Bow_primary_enhanced(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow Secondary"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
    
    def apply(self, target):
        Slowed(500, 0.3, self.game, target)

class Bow_q_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillQ"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.rect=self.rect.inflate(-33, -33)
    def apply(self, target):
        Slowed(1000, 0.6, self.game, target)

class Bow_e_skill(Player_projectiles):
    def __init__(self, pos, direction, game):
        self.source = "Bow SkillE"
        self.name = self.__class__.__name__
        super().__init__(pos, direction, game)
        self.wall_piercing = True
    
    def apply(self, target):
        Stunned(3000, self.game, target)
        Bow_explosion(self.rect.center, self.game, self.game.player.atk)

class Bazooka_e_skill(Player_projectiles, Tracking):
    def __init__(self, pos, direction, game):
        Player_projectiles.__init__(self, pos, direction, game)
        Tracking.__init__(self)
        
        self.source = "Bazooka SkillE"
        self.name = self.__class__.__name__
        self.wall_piercing = False
        self.tracking = True
        self.target = self.find_nearest_enemy()
        self.spd = 600
        self.path = []
        self.path_index = 0

        if self.target:
            self.update_path()

    def find_nearest_enemy(self):
        enemies = [e for e in self.game.enemy_sprites if not getattr(e, "ghost", False)]
        if not enemies:
            return None
        my_pos = pygame.Vector2(self.rect.center)
        return min(enemies, key=lambda e: (pygame.Vector2(e.rect.center) - my_pos).length())

    def update_path(self):
        if self.target:
            start = self.grid_pos(self.rect.center)
            goal = self.grid_pos(self.target.rect.center)
            self.path = self.astar_path(start, goal)
            self.path_index = 0

    def update(self, dt):
        # Recalculate path if tracking and target is alive
        if self.tracking and self.target and self.target.alive():
            if self.path_index >= len(self.path):
                self.update_path()
            if self.path and self.path_index < len(self.path):
                next_cell = self.path[self.path_index]
                next_pos = (next_cell[0]*self.cell_size + self.cell_size//2,
                            next_cell[1]*self.cell_size + self.cell_size//2)
                move_vec = pygame.Vector2(next_pos) - pygame.Vector2(self.rect.center)
                if move_vec.length() < 5:
                    self.path_index += 1
                else:
                    self.direction = move_vec.normalize()
        else:
            self.tracking = False  # Stop tracking if target is gone

        # Move
        self.rect.center += self.direction * self.spd * dt
        self.image_rect.center = self.rect.center

        # Wall collision (stop if hit wall)
        for wall in self.game.collision_sprites:
            if self.rect.colliderect(wall.rect):
                self.kill()
                return

        # Enemy collision (block by first enemy hit)
        for enemy in self.game.enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                self.apply(enemy)
                self.kill()
                return

        # Lifetime
        self.lifetime -= dt * 1000
        if self.lifetime <= 0:
            self.kill()

    def apply(self, target):
        Bow_explosion(self.rect.center, self.game, self.game.player.atk)