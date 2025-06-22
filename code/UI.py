import pygame
from setting import *
from data import skill_stats, entity_stats

class UI:
    def __init__(self, user, player, display_surface):
        self.user = user
        self.player = player
        self.display_surface = display_surface

        # Fonts
# Fonts
        self.font = pygame.font.SysFont("Segoe UI", 20, bold=True)
        self.level_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.cooldown_font = pygame.font.SysFont("Segoe UI", 18, bold=True)

        # Health bar (moved to the right)
        self.health_rect = pygame.Rect(60, 20, 200, 24)

        # Skill boxes
        self.skill_size = (48, 48)
        self.skill_positions = {
            "Q": pygame.Rect(WINDOW_WIDTH - 140, WINDOW_HEIGHT - 80, *self.skill_size),
            "E": pygame.Rect(WINDOW_WIDTH - 70,  WINDOW_HEIGHT - 80, *self.skill_size),
        }
        self.skill_icons = {
            "Left": pygame.image.load(os.path.join('images', 'projectiles','Gauntlet', 'Primary', '0.png')),
            "Right": pygame.image.load(os.path.join('images', 'projectiles','Gauntlet', 'Secondary', '0.png')),
            "Q": pygame.image.load(os.path.join('images', 'projectiles','Gauntlet', 'SkillQ', '0.png')),
            "E": pygame.image.load(os.path.join('images', 'projectiles','Gauntlet', 'SkillE', '0.png')),
        }

        # Health values
        self.max_hp = self.player.maxhp
        self.display_hp = self.player.hp
        self.hp_delay_speed = 100


    def draw_health_bar(self, dt):
        pygame.draw.rect(self.display_surface, (255, 255, 255), self.health_rect, width=2, border_radius=8)
        inner_rect = self.health_rect.inflate(-4, -4)
        pygame.draw.rect(self.display_surface, (30, 30, 30), inner_rect, border_radius=6)

        current_hp = max(0, min(self.player.hp, self.max_hp))

        # Smooth transition of delayed HP bar
        if self.display_hp > current_hp:
            self.display_hp -= self.hp_delay_speed * dt
            if self.display_hp < current_hp:
                self.display_hp = current_hp
        elif self.display_hp < current_hp:
            self.display_hp = current_hp

        green_width = int(inner_rect.width * (current_hp / self.max_hp))
        red_width = int(inner_rect.width * (self.display_hp / self.max_hp))

        red_rect = pygame.Rect(inner_rect.left, inner_rect.top, red_width, inner_rect.height)
        green_rect = pygame.Rect(inner_rect.left, inner_rect.top, green_width, inner_rect.height)

        pygame.draw.rect(self.display_surface, (200, 50, 50), red_rect, border_radius=6)
        pygame.draw.rect(self.display_surface, (50, 200, 50), green_rect, border_radius=6)

        text = self.font.render(f"{int(current_hp)}/{self.max_hp}", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.health_rect.center)
        self.display_surface.blit(text, text_rect)



    def draw_level_circle(self):
        # Render text
        text = self.level_font.render(f"{self.player.level}", True, (255, 255, 255))
        text_rect = text.get_rect()

        # Circle radius
        padding = 12
        radius = max(text_rect.width, text_rect.height) // 2 + padding

        # Position to the left of health bar with slight overlap
        overlap = 8
        center_x = self.health_rect.left - radius + overlap
        center_y = self.health_rect.centery

        # Draw circle background
        pygame.draw.circle(self.display_surface, (60, 60, 60), (center_x, center_y), radius)
        pygame.draw.circle(self.display_surface, (255, 255, 255), (center_x, center_y), radius, width=2)

        # Blit centered text
        text_pos = text.get_rect(center=(center_x, center_y))
        self.display_surface.blit(text, text_pos)


    def draw_skill_boxes(self, dt):
        skill_keys = ['Left', 'Right', 'Q', 'E']

        for index, key in enumerate(skill_keys):
            if key not in self.player.skills:
                continue

            skill = self.player.skills[key]

            # Compute cooldown logic
            if skill.casting:
                cooldown_ratio = skill.remaining / skill.cast_time if skill.cast_time else 0
                cooldown_time = int(skill.remaining / 1000) + 1
            elif not skill.ready:
                cooldown_ratio = skill.remaining / skill.cooldown if skill.cooldown else 0
                cooldown_time = int(skill.remaining / 1000) + 1
            else:
                cooldown_ratio = 0
                cooldown_time = 0

            cooldown_ratio = max(0, min(cooldown_ratio, 1))

            # Box position
            x = 30 + index * 70
            y = WINDOW_HEIGHT - 70
            box_rect = pygame.Rect(x, y, 60, 60)

            # Blinking effect during cooldown
            blink = int(pygame.time.get_ticks() / 300) % 2 == 0
            if skill.ready:
                bg_color = (200, 200, 200)
            elif blink:
                bg_color = (90, 90, 90)
            else:
                bg_color = (60, 60, 60)

            # Draw background box
            pygame.draw.rect(self.display_surface, bg_color, box_rect, border_radius=8)

            # Draw icon always, but with dark overlay if not ready
            if key in self.skill_icons:
                icon = pygame.transform.scale(self.skill_icons[key], (48, 48))
                self.display_surface.blit(icon, (x + 6, y + 6))
                if not skill.ready:
                    overlay = pygame.Surface((48, 48), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 120))
                    self.display_surface.blit(overlay, (x + 6, y + 6))

            # Fill overlay for cooldown (bottom-up)
            if not skill.ready:
                fill_height = int(60 * cooldown_ratio)
                fill_rect = pygame.Rect(x, y + (60 - fill_height), 60, fill_height)
                pygame.draw.rect(self.display_surface, (100, 100, 100), fill_rect, border_radius=8)

            # Border
            pygame.draw.rect(self.display_surface, (255, 255, 255), box_rect, width=2, border_radius=8)

            # Key label with shadow
            label_color = 'black' if skill.ready else 'white'
            label = self.font.render(key, True, label_color)
            shadow = self.font.render(key, True, 'gray20')
            label_rect = label.get_rect(center=(x + 30, y + 48))
            shadow_rect = shadow.get_rect(center=(x + 31, y + 49))
            self.display_surface.blit(shadow, shadow_rect)
            self.display_surface.blit(label, label_rect)

            # Cooldown text (centered)
            if cooldown_time > 0:
                cd_text = self.cooldown_font.render(str(cooldown_time), True, 'white')
                cd_shadow = self.cooldown_font.render(str(cooldown_time), True, 'black')
                cd_rect = cd_text.get_rect(center=(x + 30, y + 16))
                cd_shadow_rect = cd_text.get_rect(center=(x + 31, y + 17))
                self.display_surface.blit(cd_shadow, cd_shadow_rect)
                self.display_surface.blit(cd_text, cd_rect)


    def update(self, dt):
        self.draw_health_bar(dt)
        self.draw_level_circle()
        self.draw_skill_boxes(dt)
