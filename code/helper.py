from setting import *
import heapq
import random

class Tracking:
    def __init__(self, game, moving_sprite, target_sprite, cell_size=32):
        self.game = game
        self.map_layout = game.map_layout  # 2D grid: 0=walkable, 1=blocked
        self.cell_size = cell_size
        self.moving_sprite = moving_sprite
        self.target_sprite = target_sprite

    def grid_pos(self, pos):
        return (int(pos[0] // self.cell_size), int(pos[1] // self.cell_size))

    def is_blocked(self, pos):
        x, y = pos
        if y < 0 or y >= len(self.map_layout) or x < 0 or x >= len(self.map_layout[0]):
            return True
        return self.map_layout[y][x] == 1

    def astar_path(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

        open_set = []
        heapq.heappush(open_set, (heuristic(start, goal), 0, start, [start]))
        closed_set = set()

        while open_set:
            _, cost, current, path = heapq.heappop(open_set)
            if current == goal:
                return path
            if current in closed_set:
                continue
            closed_set.add(current)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = (current[0]+dx, current[1]+dy)
                if neighbor in closed_set or self.is_blocked(neighbor):
                    continue
                heapq.heappush(open_set, (cost+1+heuristic(neighbor, goal), cost + 1, neighbor, path+[neighbor]))
        return []

    def get_path(self):
        start = self.grid_pos(self.moving_sprite.rect.center)
        goal = self.grid_pos(self.target_sprite.rect.center)
        return self.astar_path(start, goal)

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

class Flyout_number(pygame.sprite.Sprite): # OR TEXTS
    def __init__(self, pos, number, color, game, font_size=30):
        super().__init__(game.all_sprites)
        self.image = pygame.font.Font(None, font_size).render(str(number), True, color)
        self.image_rect = self.image.get_frect(center=pygame.Vector2(pos) 
                                               + pygame.Vector2(1, 0).rotate(random.randrange(0, 360) * random.randrange(0, 20)))
        self.lifetime = 0.5
        self.spawn_time = pygame.time.get_ticks()
        self.type = 'top'
    
    def update(self, dt):
        elapsed_time = pygame.time.get_ticks() - self.spawn_time
        if elapsed_time < self.lifetime * 1000:
            self.image_rect.y -= 50 * dt
            alpha = max(0, 255 - int((elapsed_time / (self.lifetime * 1000)) * 255))
            self.image.set_alpha(alpha)
        else:
            self.kill()