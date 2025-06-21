from skills import Skill
import enemy_projectiles as eproj
import aoe
import aoe_warning as aoew
from setting import *
from status import *

class Karthus_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        eproj.Karthus_Primary(self.user, self.user.direction, self.user.game)
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
        self.user.channeling = True

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.user.channeling = False
        
class Chogath_stomp(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        aoew.Spawn_rupture(self.user.player.rect.center, self.user.game, self.user.atk)
        self.user.state = 'Attacking'
        self.user.channeling = True

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.user.channeling = False

class Veigar_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)

    def activate(self):
        super().activate()
        eproj.Veigar_Primary(self.user, self.user.direction, self.user.game)
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
        
        dir = self.user.direction.copy()
        
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

        pos = pygame.Vector2(self.game.player.rect.center) + pygame.Vector2(1, 0).rotate(randrange(0, 360))

        aoew.Spawn_darkmatter(pos, self.game, self.user.atk)
        self.user.state = 'Attacking'
        self.user.channeling = True

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.user.channeling = False

class Lulu_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        eproj.Lulu_Primary(self.user, self.user.direction, self.user.game)
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
        
    def deactivate(self):
        super().deactivate()
        
        for enemy in self.game.enemy_sprites:
            enemy.status.add(Buff(2000, 0.5, 'spd', self.game, enemy))
            enemy.status.add(Buff(5000, 0.3, 'atk', self.game, enemy))
            
        self.user.state='Walking'

