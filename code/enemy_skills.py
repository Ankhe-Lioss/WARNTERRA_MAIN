from skills import Skill
import enemy_projectiles as eproj
import aoe
import aoe_warning as aoew
from setting import *
from status import *
import random

class Karthus_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        eproj.Karthus_Primary(self.user, self.user.facing_dir, self.user.game)
        self.user.state='Attacking'
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'
        
class Poro_stomp(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        aoe.Poro_Stomp(self.user.rect.center,self.user.game,self.user.atk)
        self.user.state = 'Attacking'
        self.user.meditating = True

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.user.meditating = False

class Chogath_stomp(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        aoew.Spawn_rupture(self.user.player.rect.center, self.user.game, self.user.atk)
        self.user.state = 'Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'

class Lulu_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        
        deviation = random.randint(0, 30)
        
        eproj.Lulu_Primary(self.user, self.user.facing_dir.rotate(15).rotate(deviation), self.user.game)
        eproj.Lulu_Primary(self.user, self.user.facing_dir.rotate(-15).rotate(deviation), self.user.game)
        self.user.state='Attacking'
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Lulu_buff(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Attacking'
        for enemy in self.game.enemy_sprites:
            Buff(2000, 0.5, 'spd', self.game, enemy)
            Buff(4000, 0.3, 'atk', self.game, enemy)
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Nocturne_sprint(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Attacking'
        self.target_pos = pygame.Vector2(self.game.player.rect.center) + pygame.Vector2(random.randint(0, 100)).rotate(random.randrange(0, 360))
        self.user.attacked = False
        spd = (pygame.Vector2(self.target_pos) - pygame.Vector2(self.user.rect.center)).length() / self.cast_time * 1000
        dir = (pygame.Vector2(self.target_pos) - pygame.Vector2(self.user.rect.center)).normalize()
        self.user.forced_moving = True
        self.user.mode = {
            "dir" : dir,
            "spd" : spd
        }
        
    def deactivate(self):
        super().deactivate()        
        self.user.state='Walking'
        self.user.forced_moving = False
        self.user.mode = None

class Maokai_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        eproj.Maokai_Primary(self.user, self.user.facing_dir, self.user.game)
        self.user.heal(self.user.maxhp * 0.5)
        self.user.state='Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'


# Veigar

class Veigar_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        eproj.Veigar_Primary(self.user, self.user.facing_dir, self.user.game)
        self.user.state='Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Veigar_secondary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
    
    def activate(self):
        super().activate()
        
        dir = self.user.facing_dir.copy()
        
        eproj.Veigar_Secondary(self.user, dir, self.user.game)
        eproj.Veigar_Secondary(self.user, dir.rotate(18), self.user.game)
        eproj.Veigar_Secondary(self.user, dir.rotate(-18), self.user.game)
        eproj.Veigar_Secondary(self.user, dir.rotate(36), self.user.game)
        eproj.Veigar_Secondary(self.user, dir.rotate(-36), self.user.game)
        
        self.user.state='Attacking'
    
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'
        
class Veigar_ult(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        eproj.Veigar_Ult(self.user, self.user.game)
        self.user.state='Attacking'
    
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'
      
class Veigar_aoe(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        if self.user.phase == 1:
            for _ in range(2):
                pos = pygame.Vector2(self.game.player.rect.center) + pygame.Vector2(random.randint(0, 160), 0).rotate(randrange(0, 360))
                aoew.Spawn_darkmatter(pos, self.game, self.user.atk)
        else:
            pos = pygame.Vector2(self.game.player.rect.center) + pygame.Vector2(random.randint(0, 120), 0).rotate(randrange(0, 360))
            aoew.Spawn_darkmatter(pos, self.game, self.user.atk)

        self.user.state = 'Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'

class Veigar_cage(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        # Example: ring around player with outer radius 120, inner radius 80
        self.cage = eproj.Veigar_Cage(self.user.player.rect.center, outer_radius=240, inner_radius=220, game=self.user.game)
        self.user.state = 'Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.cage.kill()

# Soraka

class Soraka_heal(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Healing'
        if self.game.spawn_numb == 2: #only boss and check in
            self.user.heal(self.user.atk * 1)
            return
        
        target = random.choice(list(self.game.enemy_sprites))
        for enemy in self.game.enemy_sprites:
            if enemy.hp / enemy.maxhp < target.hp / target.maxhp and enemy is not self.user:
                target = enemy
        target.heal(self.user.atk * 2)
        Buff(2000, 1.5, 'spd', self.game, target)
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Soraka_ult(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Healing'
        
        for enemy in self.game.enemy_sprites:
            if enemy is self.user:
                enemy.heal(self.user.atk * 0.5)
            else:
                enemy.heal(self.user.atk * 1.5)
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Soraka_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Attacking'
        
        deviation = pygame.Vector2(random.randint(0, 160), 0).rotate(random.randrange(0, 360))
        aoew.Spawn_Soraka_star(pygame.Vector2(self.game.player.rect.center) + deviation, self.game, self.user.atk)
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

class Soraka_cc(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        self.user.state='Attacking'
        
        aoew.Spawn_Soraka_cc(self.game.player.rect.center, self.game, self.user)
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'

# Summon Buffs

class Summon_healing_buff(Skill):
    def __init__(self, user, pos, game):
        self.name = self.__class__.__name__
        self.pos = pos
        super().__init__(user, game)
        self.passive = True
        
    def activate(self):
        super().activate()
        self.buff = eproj.Healing_Buff(self.user, self.pos, self.game, self)    

class Summon_speed_buff(Skill):
    def __init__(self, user, pos, game):
        self.name = self.__class__.__name__
        self.pos = pos
        super().__init__(user, game)
        self.passive = True
        
    def activate(self):
        super().activate()
        self.buff = eproj.Speed_Buff(self.user, self.pos, self.game, self)

class Summon_attack_buff(Skill):
    def __init__(self, user, pos, game):
        self.name = self.__class__.__name__
        self.pos = pos
        super().__init__(user, game)
        self.passive = True

    def activate(self):
        super().activate()
        self.buff = eproj.Attack_Buff(self.user, self.pos, self.game, self)

