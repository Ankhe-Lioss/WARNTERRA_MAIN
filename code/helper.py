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

class Flyout_number(pygame.sprite.Sprite):
    def __init__(self, pos, number, color, game, font_size=13):
        super().__init__(game.all_sprites)
        font_path = "images/font/PressStart2P.ttf"
        font = pygame.font.Font(font_path, font_size)
        self.image = font.render(str(number), True, color)
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
            
class Announcement(pygame.sprite.Sprite):
    def __init__(self, game, text, duration=2.5, font_size=24, color=(255, 255, 255)):
        super().__init__(game.all_sprites)  # Use a separate UI group if you have one
        self.game = game
        self.text = text
        self.duration = duration
        self.elapsed = 0
        self.fade_time = 0.5  # time spent fading out (in seconds)

        # Load font and render
        self.font = pygame.font.Font("images/font/PressStart2P.ttf", font_size)
        self.image = self.font.render(text, True, color)
        self.alpha = 255
        self.image.set_alpha(self.alpha)

        # Position at bottom center of screen

        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH // 2,WINDOW_HEIGHT - 20))

    def update(self, dt):
        self.elapsed += dt

        # Fade out over last self.fade_time seconds
        if self.elapsed > self.duration:
            fade_elapsed = self.elapsed - self.duration
            fade_ratio = fade_elapsed / self.fade_time
            self.alpha = max(0, 255 * (1 - fade_ratio))
            self.image.set_alpha(int(self.alpha))

        if self.elapsed > self.duration + self.fade_time:
            self.kill()

class Description:
    def __init__(self, *parts, font_size=24, default_color=(255, 255, 255)):
        self.font = pygame.font.Font("images/font/UncialAntiqua-Regular.ttf", font_size)
        self.parts = parts
        self.default_color = default_color

        # Render 
        rendered = []
        for part in self.parts:
            if isinstance(part, tuple):
                text, color = part
            else:
                text, color = part, self.default_color
            rendered.append(self.font.render(str(text), True, color))

        # Combine into one surface
        width = sum(img.get_width() for img in rendered)
        height = max(img.get_height() for img in rendered)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        x = 0
        for img in rendered:
            self.image.blit(img, (x, 0))
            x += img.get_width()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # Default position

    def set_pos(self, pos):
        self.rect.center = pos