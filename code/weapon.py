from setting import *
from player_skills import *
import math

class Weap(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.player = game.player
        # Init
        self.surf = pygame.image.load(os.path.join('images', 'weapon', f'{self.name}.png')).convert_alpha()
        self.image = self.surf
        self.image_rotate=self.surf.copy()
        self.image_rect = self.image.get_frect(center=self.player.image_rect.center)
        self.skill_bar=game.skill_bar
        # Import skills
        self.cooldown_font = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.font = pygame.font.SysFont("Segoe UI", 17, bold=True)
        self.type= "weap"

        original_width, original_height = self.surf.get_size()
        scale_ratio = min(64 / original_width, 64 / original_height)
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)

        self.icon = pygame.transform.smoothscale(self.surf, (new_width, new_height))
        self.icon_rect = self.icon.get_frect(center=(1191,651))

    def update_pos(self):
        weapon_offset = pygame.math.Vector2(10, -30)  # adjust for hand position
        dx = self.player.facing_dir.x
        dy = self.player.facing_dir.y
        weapon_angle = math.degrees(math.atan2(-dy, dx))  -90# negative dy because of screen coords

        # Rotate weapon image
        rotated_weapon = pygame.transform.rotate(self.image_rotate, weapon_angle)
        self.image=rotated_weapon
        # Update position (adjust for rotated image center)

        self.image_rect = rotated_weapon.get_frect(center=self.player.image_rect.center + weapon_offset.rotate(-weapon_angle))


    def draw_skill_bar(self):
        surf = self.skill_bar
        base_x, base_y = 894, 571  # top-left of vine UI
        self.game.display_surface.blit(surf, (base_x, base_y))
        skill_keys = {'Left': self.primary, 'Right': self.secondary, 'Q': self.q_skill, 'E': self.e_skill}

        for index, key in enumerate(skill_keys):
            skill = skill_keys[key]
            cooldown_ratio = skill.remaining / skill.cooldown if skill.cooldown else 0

            cooldown_time = skill.remaining / 1000
            if cooldown_time > 0.9:
                cooldown_time = int(cooldown_time) + 1
            else:
                cooldown_time = int(cooldown_time * 10) / 10.0

            cooldown_ratio = max(0, min(cooldown_ratio, 1))

            x = base_x + 41 + index * 53
            y = base_y + 46
            icon_rect = pygame.Rect(x, y, 42, 42)


            # Background (only visible if icon has transparency)
            bg_color = (200, 200, 200)
            pygame.draw.rect(self.game.display_surface, bg_color, icon_rect, border_radius=6)

            # Resize and draw skill icon to 42x42
            self.game.display_surface.blit(skill.icon, icon_rect)
            # Cooldown overlay
            if not skill.ready:
                overlay = pygame.Surface((42, 42), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                self.game.display_surface.blit(overlay, icon_rect.topleft)

                fill_height = int(42 * cooldown_ratio)
                fill_rect = pygame.Rect(x, y + (42 - fill_height), 42, fill_height)
                if not skill.casting:
                    pygame.draw.rect(self.game.display_surface, (80, 80, 80), fill_rect, border_radius=6)

            # Key Label (below icon)
            label_color = 'bisque' if skill.ready else 'gray'
            label = self.font.render(key, True, label_color)
            label_rect = label.get_rect(center=(x + 21, y + 55))
            self.game.display_surface.blit(label, label_rect)

            # Cooldown text (top-center)
            if cooldown_time > 0 and not skill.casting:
                cd_text = self.cooldown_font.render(str(cooldown_time), True, 'white')
                cd_rect = cd_text.get_rect(center=(x + 21, y + 17))
                self.game.display_surface.blit(cd_text, cd_rect)
        self.game.display_surface.blit(self.icon,self.icon_rect.topleft)
        if self.player.swap_cooldown>0:
            center_pos=self.icon_rect.center
            radius=40*(self.player.swap_cooldown/self.player.swap_maxcooldown)
            # 1. Create a transparent surface
            circle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

            # 2. Draw the circle centered on that surface
            light_gray = (245, 245, 245, 60)  # RGBA: light gray + transparency
            pygame.draw.circle(circle_surf, light_gray, (int(radius), int(radius)), int(radius))

            # 3. Compute the top-left to blit so the circle is centered at center_pos
            blit_pos = (center_pos[0] - radius, center_pos[1] - radius)

            # 4. Blit to the target surface (e.g., the screen)
            self.game.display_surface.blit(circle_surf, blit_pos)
    def update(self, dt):
        self.update_pos()


        if self.game.player.weap is self:
            self.visible=True
            self.draw_skill_bar()
        else:
            self.visible=False
        self.primary.update(dt)
        self.secondary.update(dt)
        self.q_skill.update(dt)
        self.e_skill.update(dt)

class Gauntlet(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)

        # Import skills
        self.primary = Gauntlet_primary(self.player, self.game)
        self.q_skill = Gauntlet_q_skill(self.player, self.game)
        self.e_skill = Gauntlet_e_skill(self.player, self.game)
        self.secondary = Gauntlet_secondary(self.player, self.game)


class Bow(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)

        # Import skills
        self.primary = Bow_primary(self.player, self.game)
        self.q_skill = Bow_q_skill(self.player, self.game)
        self.e_skill = Bow_e_skill(self.player, self.game)
        self.secondary = Bow_secondary(self.player, self.game)

class Bazooka(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)

        # Import skills
        self.primary = Bazooka_primary(self.player, self.game)
        self.q_skill = Bazooka_q_skill(self.player, self.game)
        self.e_skill = Bazooka_e_skill(self.player, self.game)
        self.secondary = Bazooka_secondary(self.player, self.game)