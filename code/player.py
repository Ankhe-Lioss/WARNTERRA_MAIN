from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, game):
        
        # Initializing
        super().__init__(group)
        self.game = game
        
        # Loading stats
        self.stats = entity_stat["Player"]
        self.pos = pos
        
        # States
        self.facing = ("up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left")
        self.facing_state = "right"
        self.frame_index = 0
        
        # Loading appearance
        self.frames = dict()
        self.load_images()
        self.image = self.frames[self.facing_state][self.frame_index]
    
    def update_image(self):
        self.image = self.frames[self.facing_state][self.frame_index]
    
    def get_state(self):
        # Calculate mouse position references
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        facing_dir = mouse_pos - player_pos
        angle = - degrees(atan2(facing_dir.x, facing_dir.y)) + 180
        
        self.facing_state = self.facing[int((angle + 22.5 if angle <= 337.5 else angle + 22.5 - 360) / 45)]
        self.update_image()

    def load_images(self):
        for key in self.facing:
            self.frames[key] = []
            for i in range(4):
                surf = pygame.image.load(os.path.join("images", "player", key, f"{i}.png"))
                self.frames[key].append(surf)
    
    def draw(self):
        self.game.display_surface.blit(self.image, self.pos)
        
        