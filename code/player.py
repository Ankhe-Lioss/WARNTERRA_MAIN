from setting import *
from entity import Entity
from player_skills import PlayerSkills
from health_bar import *
from weapon import *
class Player(Entity):
    def __init__(self, pos, game):
        self.name = "Player"
        self.weapon_type = "gauntlet"  # <- make sure this is first
        self.image_offset = (0, -15)
        super().__init__(game.player_sprites, game)
        self.game = game
        self.pos = pos
        # Skill setup
        skills_obj = PlayerSkills(self, game)
        self.skills_gauntlet = skills_obj.skills_gauntlet
        self.skills_bow = skills_obj.skills_bow
        
        # Attach current skill set based on weapon
        self.skills = self.skills_gauntlet if self.weapon_type == "gauntlet" else self.skills_bow

        # States
        self.facing = ("up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left")
        self.facing_state = "right"
        self.frame_index = 0
        
        # Loading appearance
        self.frames = dict()
        self._load_images()
        self.image: pygame.Surface = self.frames[self.facing_state][self.frame_index]
        self.rect = self.image.get_frect(center=self.pos)
        self.image_rect = self.rect.copy()
        self.player_health_bar=Player_healthbar(self)
        self.rect = self.rect.inflate(0, -30)

        self.image_rect.center = (pygame.math.Vector2(self.rect.center) + self.image_offset)

        self.weapons=[]
        self.current_weapon_index = 0
        self.swap_cooldown = 0  # in milliseconds
        self.swap_maxcooldown = 2000
        # Hitbox
        self.direction = pygame.Vector2()
    def joystick_input(self):

        if self.game.have_joystick == True:

            self.joystick=self.game.joystick
        else:
            return
        # Handle right stick (assumed for facing direction)
        right_x = self.joystick.get_axis(2)
        right_y = self.joystick.get_axis(3)

        self.facing_dir.x = right_x if abs(right_x) >= 0.07 else 0
        self.facing_dir.y = right_y if abs(right_y) >= 0.07 else 0

        if self.facing_dir.length_squared() > 0:
            self.facing_dir = self.facing_dir.normalize()
        else:
            self.facing_dir = pygame.Vector2(0,1)
        # D-pad (hat) input for movement direction
        hat_x, hat_y = self.joystick.get_hat(0)
        self.direction.x = hat_x
        self.direction.y = -hat_y  # Flip Y for game world
        move_x = self.joystick.get_axis(0)
        move_y = self.joystick.get_axis(1)

        self.direction.x += move_x if abs(move_x) >= 0.07 else 0
        self.direction.y += move_y if abs(move_y) >= 0.07 else 0

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        if hasattr(self,'weap'):
            if self.joystick.get_button(4):
                self.weap.primary.cast()
            if self.joystick.get_button(5):
                self.weap.secondary.cast()
            if self.joystick.get_axis(4) > 0.5:
                self.weap.q_skill.cast()
            if self.joystick.get_axis(5) > 0.5:
                self.weap.e_skill.cast()
    def update_animation(self, dt):
        self.frame_index = self.frame_index + 10 * dt if self.direction and not self.stunned else 0
        self.image = self.frames[self.facing_state][int(self.frame_index) % len(self.frames[self.facing_state])]
            
    
    def update_facing(self):
        # Calculate mouse position references
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(CENTER)
        self.facing_dir = (mouse_pos - player_pos)
        self.facing_dir = self.facing_dir.normalize() if self.facing_dir else self.facing_dir
    def update_facing_state(self):
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
        #skill input
        if hasattr(self,'weap'):
            if pygame.mouse.get_pressed()[0]:
                self.weap.primary.cast()
            if pygame.mouse.get_pressed()[2]:
                self.weap.secondary.cast()
            if pygame.key.get_pressed()[pygame.K_q]:
                self.weap.q_skill.cast()
            if pygame.key.get_pressed()[pygame.K_e]:
                self.weap.e_skill.cast()
            if keys[pygame.K_TAB] and self.swap_cooldown <= 0 and len(self.weapons)>1:
                self.current_weapon_index = (self.current_weapon_index + 1) % len(self.weapons)
                self.weap = self.weapons[self.current_weapon_index]
                self.swap_cooldown = self.swap_maxcooldown

    def take_damage(self, dmg, pen=0, type="normal"):
        super().take_damage(dmg, pen, type)
        # animate hit:
        self.take_dmg_animation_remaining = 100
        self.taking_dmg = True
    
    def death(self):
        self.game.game_state = "in_death_menu"
        self.game.pausing=True

    def collide_with_enemies(self, dt):
        for enemy in self.game.enemy_sprites:
            if not enemy.ghost and self.rect.colliderect(enemy.rect):
                self.forced_moving = True
                dir = (pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center))
                self.mode = {"spd" : 800, "dir" : dir.normalize() if dir else dir, "type" : "knockback"}
                self.knockback_remaining = 0.1
                if enemy.name == 'Nocturne' and enemy.state == 'Attacking' and not enemy.attacked:
                    enemy.attacked = True
                    self.take_damage(enemy.atk)
            
        
        if self.forced_moving:
            if self.mode["type"] != "knockback":
                return
            
            self.knockback_remaining -= dt
            if self.knockback_remaining <= 0:
                self.forced_moving = False
                self.mode = None
                self.knockback_remaining = 0

    def update(self, dt):
        # mouse and keyboard
        self.input()
        self.update_facing()
        # controller
        self.joystick_input()
        # update facing
        self.player_health_bar.update(dt)
        if not self.stunned:
            self.update_facing_state()
        # move with entity

        super().update(dt)  # move
        # animation update
        """for skill in self.skills.values():
            skill.update(dt)"""

        self.update_animation(dt)
        self.collide_with_enemies(dt)
        # Update swap cooldown
        if self.swap_cooldown > 0:
            self.swap_cooldown -= dt * 1000  # dt is in seconds
            if self.swap_cooldown < 0:
                self.swap_cooldown = 0


import heapq

def A_star_tracking(grid, rect, goal_pos):
    entity_w_tiles = int(rect.width // TILE_SIZE)
    entity_h_tiles = int(rect.height // TILE_SIZE)
    def to_tile(pos):
        return int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)

    def is_walkable_at(x, y):
        # Simulate placing the full rect at tile (x, y)
        for dy in range(entity_h_tiles):
            for dx in range(entity_w_tiles):
                check_x = x + dx
                check_y = y + dy

                if not (0 <= check_x < len(grid[0]) and 0 <= check_y < len(grid)):
                    return False  # Out of bounds
                if grid[check_y][check_x] == 1:
                    return False

                # Simulate collision against sprites
                pixel_rect = pygame.Rect(
                    check_x * TILE_SIZE,
                    check_y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

        return True

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            x, y = current
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for nx, ny in neighbors:
                if is_walkable_at(nx, ny):
                    tentative_g = g_score[current] + 1
                    neighbor = (nx, ny)
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
        return []

    # Starting and goal tile are based on top-left of rect and goal center
    start_tile = to_tile(rect.topleft)
    goal_tile = to_tile(goal_pos)

    path = a_star(start_tile, goal_tile)

    if not path:
        return pygame.Vector2(0, 0)  # No path found

    next_tile = path[0]
    next_pos = pygame.Vector2(
        (next_tile[0] + 0.5) * TILE_SIZE,
        (next_tile[1] + 0.5) * TILE_SIZE
    )

    current_center = pygame.Vector2(rect.center)
    direction = next_pos - current_center
    if direction.length() > 0:
        direction = direction.normalize()

    return direction
