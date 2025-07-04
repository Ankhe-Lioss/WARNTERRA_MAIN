import pygame
import os
from setting import *
from data import skill_stats, entity_stats
from entity import Boss
from status import *

class UI:
    def __init__(self, game, player, display_surface):
        self.game = game
        self.player = player
        self.display_surface = display_surface
        self.boss_name_font=pygame.font.Font(os.path.join('images','font','UncialAntiqua-Regular.ttf'), 20)
        # Fonts
        self.font = pygame.font.Font(os.path.join('images','font','Orbitron-Regular.ttf'), 20)
        self.level_font = pygame.font.Font(os.path.join('images','font','Orbitron-Bold.ttf'), 20)
        self.cooldown_font = pygame.font.Font(os.path.join('images','font','ShareTechMono-Regular.ttf'), 20)

        # Health bar position (bottom left side)
        self.health_rect = pygame.Rect(60, WINDOW_HEIGHT - 70, 200, 24)

        # Boss HP bar (top center)
        self.boss_health_rect = pygame.Rect((WINDOW_WIDTH - 500) // 2, 50, 500, 26)

        # Skill UI
        self.skill_size = (48, 48)


        # HP smoothing
        self.display_hp = self.player.hp
        self.hp_delay_speed = 100

        self.boss_display_hp = 0
        self.current_boss = None

        #track player level
        self.last_level = self.player.level

    def draw_entity_health_bar(self, entity, rect, dt, display_hp_ref, delay_speed, color_fg, color_bg, label=None, cur=None, mx=None):
        pygame.draw.rect(self.display_surface, (255, 255, 255), rect, width=2, border_radius=6)
        inner_rect = rect.inflate(-4, -4)
        pygame.draw.rect(self.display_surface, (30, 30, 30), inner_rect, border_radius=4)

        current_hp = max(0, min(entity.hp, entity.maxhp)) if cur is None else cur
        max_hp = entity.maxhp if mx is None else mx

        if display_hp_ref[0] > current_hp:
            display_hp_ref[0] -= delay_speed * dt
            if display_hp_ref[0] < current_hp:
                display_hp_ref[0] = current_hp
        elif display_hp_ref[0] < current_hp:
            display_hp_ref[0] = current_hp

        green_width = int(inner_rect.width * (current_hp / entity.maxhp))
        red_width = int(inner_rect.width * (max_hp / entity.maxhp))

        red_rect = pygame.Rect(inner_rect.left, inner_rect.top, red_width, inner_rect.height)
        green_rect = pygame.Rect(inner_rect.left, inner_rect.top, green_width, inner_rect.height)

        pygame.draw.rect(self.display_surface, color_bg, red_rect, border_radius=4)
        pygame.draw.rect(self.display_surface, color_fg, green_rect, border_radius=4)

        if label:
            label_surf = self.boss_name_font.render(label, True, (255, 255, 255))
            label_rect = label_surf.get_rect(midbottom=(rect.centerx, rect.top - 5))
            self.display_surface.blit(label_surf, label_rect)

 # Determine font color (black for boss HP, white otherwise)
        if isinstance(entity, Boss):
            text_color = (0, 0, 0)  # black for boss bar
        else:
            text_color = (255, 255, 255)

        text = self.font.render(f"{int(entity.hp)}/{int(entity.maxhp)}", True, text_color)
        text_rect = text.get_rect(center=rect.center)
        self.display_surface.blit(text, text_rect)

    def draw_health_bar(self, dt):
        self.draw_entity_health_bar(
            entity=self.player,
            rect=self.health_rect,
            dt=dt,
            display_hp_ref=[self.display_hp],
            delay_speed=self.hp_delay_speed,
            color_fg=(50, 200, 50),
            color_bg=(200, 50, 50),
            label="PLAYER"
        )

    def draw_boss_bar(self, dt):
        boss = next((sprite for sprite in self.game.enemy_sprites if isinstance(sprite, Boss)), None)
        
        if boss is None or not boss.alive():
            self.current_boss = None
            return

        if self.current_boss != boss:
            self.current_boss = boss
            if boss.phase == 1:
                self.boss_display_hp = (boss.hp - boss.maxhp / 2) * 2
            else:
                self.boss_display_hp = boss.hp * 2
        
        self.boss_hp_delay_speed = boss.maxhp / 4
                
                # Choose background color based on phase
        if hasattr(boss, 'phase') and boss.phase >= 2:
            bg_color = (255, 255, 255)  # White for phase 2+
        else:
            bg_color = (200, 50, 50)    # Default dark red

        if boss.phase == 1:
            self.draw_entity_health_bar(
                entity=boss,
                rect=self.boss_health_rect,
                dt=dt,
                display_hp_ref=[self.boss_display_hp],
                delay_speed=self.boss_hp_delay_speed,
                color_fg=(255, 100, 100),  # Foreground always red
                color_bg=bg_color,
                label=boss.name.upper() + (f" - PHASE {boss.phase}" if hasattr(boss, 'phase') else ""),
                cur=(boss.hp - boss.maxhp / 2) * 2,
                mx=boss.maxhp
            )
        else:
            self.draw_entity_health_bar(
                entity=boss,
                rect=self.boss_health_rect,
                dt=dt,
                display_hp_ref=[self.boss_display_hp],
                delay_speed=self.boss_hp_delay_speed,
                color_fg=(200, 50, 50),  # Foreground always red
                color_bg=bg_color,
                label=boss.name.upper() + (f" - PHASE {boss.phase}" if hasattr(boss, 'phase') else ""),
                cur=boss.hp * 2,
                mx=boss.maxhp
            )

    
    def draw_level_circle(self):
        text = self.level_font.render(f"{self.player.level+1}", True, (255, 255, 255))
        padding = 12
        radius = max(text.get_width(), text.get_height()) // 2 + padding

        center_x = self.health_rect.left  # anchors to HP bar left
        center_y = self.health_rect.centery

        pygame.draw.circle(self.display_surface, (60, 60, 60), (center_x, center_y), radius)
        pygame.draw.circle(self.display_surface, (255, 255, 255), (center_x, center_y), radius, width=2)

        text_rect = text.get_rect(center=(center_x, center_y))
        self.display_surface.blit(text, text_rect)
    
    def draw_status_effects(self):
        status_bar_top = self.health_rect.bottom + 6
        icon_size = 24
        spacing = 4

        # Collect all status effects owned by player
        all_effects = [
            sprite for sprite in self.game.all_sprites
            if isinstance(sprite, Status) and sprite.owner == self.player
        ]

        # Group by unique key: name + type (to separate same-name different effects)
        grouped_effects = {}
        for effect in all_effects:
            key = effect.name + (getattr(effect, 'type', '') or '')
            if key not in grouped_effects or effect.remaining > grouped_effects[key].remaining:
                grouped_effects[key] = effect

        # Sort for consistency
        effects = sorted(grouped_effects.values(), key=lambda e: e.name + getattr(e, 'type', ''))

        for index, effect in enumerate(effects):
            # Load icon or fallback to frame
            if not effect.icon:
                continue
            icon = effect.icon

            # Draw icon
            icon_x = self.health_rect.left + index * (icon_size + spacing)
            icon_y = status_bar_top
            self.display_surface.blit(icon, (icon_x, icon_y))

            # Draw white border
            border_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
            pygame.draw.rect(self.display_surface, (255, 255, 255), border_rect, 1)

    '''def draw_skill_boxes(self, dt):
        skill_keys = ['Left', 'Right', 'Q', 'E']
        for index, key in enumerate(skill_keys):
            if key not in self.player.skills:
                continue
            skill = self.player.skills[key]

            cooldown_ratio = skill.remaining / skill.cooldown if skill.cooldown else 0
            cooldown_time = skill.remaining / 1000

            if cooldown_time > 0.9:
                cooldown_time = int(cooldown_time) + 1
            else:
                cooldown_time = int(cooldown_time * 10) / 10.0


            cooldown_ratio = max(0, min(cooldown_ratio, 1))

            # Align to bottom-right
            x = WINDOW_WIDTH - (70 * (4 - index)) - 30
            y = WINDOW_HEIGHT - 80
            box_rect = pygame.Rect(x, y, 60, 60)

            blink = int(pygame.time.get_ticks() / 300) % 2 == 0
            bg_color = (200, 200, 200) if skill.ready else (90, 90, 90 if blink else 60)

            pygame.draw.rect(self.display_surface, bg_color, box_rect, border_radius=8)

            icon = skill.icon
            self.display_surface.blit(icon, (x + 6, y + 6))
            if not skill.ready:
                overlay = pygame.Surface((48, 48), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                self.display_surface.blit(overlay, (x + 6, y + 6))

            if not skill.ready:
                fill_height = int(60 * cooldown_ratio)
                fill_rect = pygame.Rect(x, y + (60 - fill_height), 60, fill_height)
                if not skill.casting:
                    pygame.draw.rect(self.display_surface, (80, 80, 80), fill_rect, border_radius=8)

            pygame.draw.rect(self.display_surface, (255, 255, 255), box_rect, width=2, border_radius=8)

            label_color = 'bisque' if skill.ready else 'white'
            label = self.font.render(key, True, label_color)
            shadow = self.font.render(key, True, 'gray20')
            label_rect = label.get_rect(center=(x + 30, y + 48))
            shadow_rect = shadow.get_rect(center=(x + 31, y + 49))
            self.display_surface.blit(shadow, shadow_rect)
            self.display_surface.blit(label, label_rect)

            if cooldown_time > 0 and not skill.casting:
                cd_shadow = self.cooldown_font.render(str(cooldown_time), True, 'black')
                cd_text = self.cooldown_font.render(str(cooldown_time), True, 'white')
                    
                cd_rect = cd_text.get_rect(center=(x + 30, y + 16))
                cd_shadow_rect = cd_text.get_rect(center=(x + 31, y + 17))
                self.display_surface.blit(cd_shadow, cd_shadow_rect)
                self.display_surface.blit(cd_text, cd_rect)'''

    def update(self, dt):

        #self.draw_health_bar(dt)
        #self.draw_level_circle()
        #self.draw_skill_boxes(dt)
        self.draw_status_effects()
        self.draw_boss_bar(dt)

