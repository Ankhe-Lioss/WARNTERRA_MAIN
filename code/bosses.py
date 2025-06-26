from setting import *
from entity import Boss
from enemy_skills import *

class Veigar(Boss):
    def __init__(self, groups, game):
        self.name = 'Veigar'

        self.image_offset = (-20,-40)
        super().__init__(groups, game)
        self.rect=self.rect.inflate(-105,-80   )
        self.skills = {
            'primary': Veigar_primary(self, game),
            'secondary': Veigar_secondary(self, game),
            'heal1' : Summon_healing_buff(self, (200, 3500), game),
            'heal2' : Summon_healing_buff(self, (1350, 3500), game),
            'speed' : Summon_speed_buff(self, (780, 3380), game)
        }
        self.mode = 1
        self.phase = 1
        self.phase_remaining = 10000
    
    def change_phase(self):
        super().change_phase()
        self.mode = 1
        self.phase_remaining = 5000
        
        if 'primary' in self.skills:
            del self.skills['primary']
        if 'aoe' in self.skills:
            del self.skills['aoe']
        
        self.skills['ult'] = Veigar_ult(self, self.game)
        self.skills['secondary'] = Veigar_secondary(self, self.game)
        
        self.skills['secondary'].warmup = 1000
        self.skills['secondary'].cooldown = 2000
        self.phase = 2
        self.mode = 1
        self.aura=Dark_aura(2000,self.game,self)
        
    def update(self, dt):
        #print(self.skills['speed'].remaining)
        super().update(dt)
        self.phase_remaining -= dt * 1000
        if self.mode == 1 and self.phase_remaining <= 0: # 1 to 2
            self.mode = 2
            if self.phase == 1:
                del self.skills['primary']
                del self.skills['secondary']
                self.skills['aoe'] = Veigar_aoe(self, self.game)
                
                self.phase_remaining = 6000
            else:
                del self.skills['secondary']
                self.skills['aoe'] = Veigar_aoe(self, self.game)
                self.skills['cage'] = Veigar_cage(self, self.game)
                
                self.phase_remaining = 6000
                
        elif self.mode == 2 and self.phase_remaining <= 0:
            self.mode = 1
            if self.phase == 1:
                del self.skills['aoe']
                self.skills['primary'] = Veigar_primary(self, self.game)
                self.skills['secondary'] = Veigar_secondary(self, self.game)
                
                self.phase_remaining = 10000
                
            else:
                del self.skills['aoe']
                del self.skills['cage']
                self.skills['secondary'] = Veigar_secondary(self, self.game)
                self.skills['secondary'].cooldown = 1000
                
                self.phase_remaining = 10000

class Soraka(Boss):
    def __init__(self, groups, game):
        self.name = 'Soraka'
        super().__init__(groups, game)
        
        self.states.append('Healing')
        self.load_frames()
        
        self.skills = {
            'heal' : Soraka_heal(self, game),
            'aoe' : Soraka_primary(self, game),
            'cc' : Soraka_cc(self, game),
            'heal1': Summon_attack_buff(self, (110, 3230), game),
            'heal2': Summon_attack_buff(self, (1455, 3230), game),
            'atk': Summon_healing_buff(self, (780, 3390), game)
        }
        self.phase = 1
    
    def change_phase(self):
        super().change_phase()
        del self.skills['heal']
        self.skills['ult'] = Soraka_ult(self, self.game)
        
        self.game.wave += 1
        from setlevel import spawn_wave
        spawn_wave(self.game)
        self.aura=Dark_aura(2000,self.game,self)

    def update(self, dt):
        super().update(dt)
        if self.game.spawn_numb > 2:
            if self.phase == 1:
                self.invulnerable = 0.50001
            else:
                self.invulnerable = 0.01
        else:
            if hasattr(self, 'invulnerable'):
                del self.invulnerable
