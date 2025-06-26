from setting import *

class Delay:
    def __init__(self, delay_time, commands, game):
        self.delay_time = delay_time
        self.commands = commands
        self.elapsed = 0
        self.game = game
        
        # Register
        self.game.delays.add(self)
    
    def update(self, dt):
        self.elapsed += dt * 1000 
        if self.elapsed >= self.delay_time:
            self.commands()
            self.game.delays.discard(self)  
            del self