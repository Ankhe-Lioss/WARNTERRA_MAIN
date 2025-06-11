from skills import Skill
import enemy_projectiles as eproj
import aoe
import aoe_warning as aoew
from setting import *

class Karthus_primary(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.source='Karthus Primary'
        super().__init__(user, game)
        
    def activate(self):
        super().activate()
        eproj.Karthus_Primary(self.user.rect.center, self.user.direction, (self.user.game.all_sprites, self.user.game.enemy_projectiles), self.user.game)
        self.user.state='Attacking'
        
    def deactivate(self):
        super().deactivate()
        self.user.state='Walking'
        
class Poro_stomp(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.name = 'Poro_stomp'
        super().__init__(user, game)

    def activate(self):
        super().activate()
        aoe.Poro_Stomp(self.user.rect.center,self.user.game.all_sprites,self.user.game,self.user.atk)
        self.user.state = 'Attacking'

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        
class Chogath_stomp(Skill):
    def __init__(self, user, game):
        self.name = self.__class__.__name__
        self.name = 'Chogath_stomp'
        super().__init__(user, game)

    def activate(self):
        super().activate()
        aoew.Spawn_rupture(self.user.player.rect.center, self.user.game.all_sprites, self.user.game, self.user.atk)
        self.user.state = 'Attacking'
        self.user.channeling = True

    def deactivate(self):
        super().deactivate()
        self.user.state = 'Walking'
        self.user.channeling = False