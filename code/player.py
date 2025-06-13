from setting import *
from entities import Entity

class Player(Entity):
    def __init__(self, pos, game):
        self.name = "Player"
        
        # Initializing
        super().__init__(game.player_sprites, game)
        self.game = game
        
        # Loading stats
        self.pos = pos
        
        # States
        self.facing = ("up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left")
        self.facing_state = "right"
        self.frame_index = 0
        
        # Loading appearance
        self.frames = dict()
        self._load_images()
        self.image: pygame.Surface = self.frames[self.facing_state][self.frame_index]
        self.rect = self.image.get_frect(center=self.pos).inflate(-10, -10)
        
        # Hitbox
        self.direction = pygame.Vector2()
        
    
    def update_animation(self, dt):
        self.frame_index = self.frame_index + (6 * dt if self.direction and not self.stunned else 0)
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
    
    def update(self, dt):
        self.input()
        if not self.stunned:
            self.update_facing()
        
        super().update(dt) # move
        
        self.update_animation(dt)
        self.collide_with_enemies(dt)
    
    def take_damage(self, dmg, pen=0, type="normal"):
        super().take_damage(dmg, pen, type)
        # animate hit:
        self.take_dmg_animation_remaining = 100
        self.taking_dmg = True
    
    def death(self):
        self.game.running = False
        print('u loose bitchess')
    
    def collide_with_enemies(self, dt):
        for enemy in self.game.enemy_sprites:
            if not enemy.ghost and self.rect.colliderect(enemy.rect):
                self.forced_moving = True
                dir = (pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center))
                self.mode = {"spd" : 1000, "dir" : dir.normalize() if dir else dir, "type" : "knockback"}
                self.knockback_remaining = 0.02
        
        if self.forced_moving:
            if self.mode["type"] != "knockback":
                return
            
            self.knockback_remaining -= dt
            if self.knockback_remaining <= 0:
                self.forced_moving = False
                self.mode = None
                self.knockback_remaining = 0
        
        