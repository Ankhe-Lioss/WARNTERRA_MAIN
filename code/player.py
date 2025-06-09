from setting import *
from entities import entity

class Player(entity):
    def __init__(self, pos, groups, game):
        self.name = "Player"
        
        # Initializing
        super().__init__(pos, groups, game)
        self.game = game
        
        # Loading stats
        self.pos = pos
        
        # States
        self.facing = ("up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left")
        self.facing_state = "right"
        self.frame_index = 0
        
        # Other state
        self.channeling = False
        self.forced_moving = False
        self.mode = None
        
        # Loading appearance
        self.frames = dict()
        self._load_images()
        self.image: pygame.Surface = self.frames[self.facing_state][self.frame_index]
        self.rect = self.image.get_frect(center=self.pos)
        
        # Hitbox
        self.direction = pygame.Vector2()
        self.hitbox_rect = self.rect.inflate(-20, -20)
    
    def update_animation(self, dt):
        self.frame_index = self.frame_index + (6 * dt if self.direction else 0)
        self.image = self.frames[self.facing_state][int(self.frame_index) % len(self.frames[self.facing_state])]
    
    def update_facing(self):
        # Calculate mouse position references
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.facing_dir = (mouse_pos - player_pos)
        self.facing_dir = self.facing_dir.normalize() if self.facing_dir else self.facing_dir
        angle = - degrees(atan2(self.facing_dir.x, self.facing_dir.y)) + 180
        
        self.facing_state = self.facing[int((angle + 22.5 if angle <= 337.5 else angle + 22.5 - 360) / 45)]

    def _load_images(self):
        for key in self.facing:
            self.frames[key] = []
            for i in range(4):
                surf = pygame.image.load(os.path.join("images", "player", key, f"{i}.png")).convert_alpha()
                self.frames[key].append(surf)
        
    def input(self):
        """ Movement input """
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        if self.channeling:
            return
        
        self.hitbox_rect.x += self.direction.x * self.spd * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.spd * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def forced_move(self, dt):
        forced_spd = self.mode
        self.hitbox_rect.x += self.facing_dir.x * forced_spd * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.facing_dir.y * forced_spd * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def update(self, dt):
        self.input()
        self.update_facing()
        
        if self.forced_moving:
            self.forced_move(dt)
        else:
            self.move(dt) 
        self.update_animation(dt)
        