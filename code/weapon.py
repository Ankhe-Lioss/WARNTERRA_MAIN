from setting import *
from player_skills import *
import math
from button import Instruction_rect
from helper import Description

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

        #skill icon adjustment
        original_width, original_height = self.surf.get_size()
        scale_ratio = min(64 / original_width, 64 / original_height)
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        self.icon = pygame.transform.smoothscale(self.surf, (new_width, new_height))
        self.icon_rect = self.icon.get_frect(center=(1191,651))
        #instruction to check for mouse hoovering
        self.instruction_rects = {
            'Left': Instruction_rect(self.game, pygame.Rect(894 + 41 + 0 * 53, 571 + 46, 42, 42), weapon_skill_detail[self.name][0]),
            'Right': Instruction_rect(self.game, pygame.Rect(894 + 41 + 1 * 53, 571 + 46, 42, 42), weapon_skill_detail[self.name][1]),
            'Q': Instruction_rect(self.game, pygame.Rect(894 + 41 + 2 * 53, 571 + 46, 42, 42), weapon_skill_detail[self.name][2]),
            'E': Instruction_rect(self.game, pygame.Rect(894 + 41 + 3 * 53, 571 + 46, 42, 42), weapon_skill_detail[self.name][3])
        }
    
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

    #draw skill bar and anything on it including(skill, cooldown,instruction and timer)
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

            # THIS FCKING RECTDAHDUIHASDHAIUSDHAISHDIAUSDUIHD


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
        #uptate weapon skill timer
    def update_skills(self, dt):
        self.primary.update(dt)
        self.secondary.update(dt)
        self.q_skill.update(dt)
        self.e_skill.update(dt)
     
    def update_instruction_rect(self):
        for key in self.instruction_rects:
            self.instruction_rects[key].update(self.game.display_surface)
    
    def update(self, dt):
        self.update_pos()
        if self.game.player.weap is self:
            self.visible=True
            self.draw_skill_bar()
        else:
            self.visible=False
        
        self.update_instruction_rect()
        self.update_skills(dt)

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

class Lunar_gun(Weap):
    def __init__(self, game):
        self.name = self.__class__.__name__
        super().__init__(game)

        self.gun_types = ["Calibrum", "Infernum"]
        self.gun_type = "Calibrum"

        # Import skills
        self.q_skills = {
            "Calibrum" : Calibrum_skill(self.player, self.game),
            "Infernum" : Infernum_skill(self.player, self.game)
        } 
        
        self.primary = Calibrum_primary(self.player, self.game)
        self.secondary = Lunar_swap(self.player, self.game)
        self.q_skill = self.q_skills[self.gun_type]
        self.e_skill = Lunar_ult(self.player, self.game)
    
    def update_skills(self, dt):
        self.primary.update(dt)
        self.secondary.update(dt)
        self.e_skill.update(dt)
        
        for gun_type in self.gun_types:
            self.q_skills[gun_type].update(dt)

Weapon_Dict = {
    "Bow": Bow,
    "Gauntlet": Gauntlet,
    "Bazooka" : Bazooka,
    "Lunar_gun" : Lunar_gun
}

CC = (130, 60, 220)
ATK = (255, 255, 100)
WHITE = (255, 255, 255)
SCALE = (150, 220, 220)
TIME = (220, 160, 130)
ICY = (90, 200, 255)
CALIBRUM = (90, 240, 180)
INFERNUM = (50, 80, 200)

weapon_skill_detail = {
    "Gauntlet": [
        Description(
            ("Rising Spell Force\n", WHITE, 28),
            ("Fires a bolt of magic energy that strikes the first enemy hit, dealing damage equal to "),
            (f"{player_projectiles["Gauntlet_primary"][0] * 100:.0f}% of ATK", ATK),
            (".")
                    ),
        Description(
            ("Arcane shift\n", WHITE, 28),
            ("Dashes a short distance toward the cursor.")
                    ),
        Description(
            ("Mystic Shot", WHITE, 28),
            ("\n"),
            ("Unleashes a mighty arcane beam upon the first enemy struck, dealing "),
            (f"{player_projectiles["Gauntlet_q_skill"][0] * 100:.0f}% of ATK", ATK),
            (" as damage. On hit, this skill and Skill E have their cooldowns reduced by "),
            ("2 seconds", TIME),
            (", and the Right Skill is immediately refreshed.")
                    ),
        Description(
            ("Trueshot barrage\n", WHITE, 28),
            ("Unleashes a colossal surge of energy that cuts through all obstacles, striking every enemy in its path for "),
            (f"{player_projectiles["Gauntlet_e_skill"][0] * 100:.0f}% of ATK", ATK),
            (" as damage and "),
            ("slowing", CC),
            (" them by "),
            (f"75%", SCALE),
            (" for "),
            ("2 seconds", TIME),
            (".")
        )
    ],
    "Bow" : [
        Description(
            ("Frost shot\n", WHITE, 28),
            ("Fires a chilling arrow that deals "),
            (f"{player_projectiles['Bow_primary'][0] * 100:.0f}% of ATK", ATK),
            (" as damage to the first enemy hit, "),
            ("slowing", CC),
            (" them by "),
            ("20%", SCALE),
            (" for "),
            ("0.5 seconds", TIME),
            (".\n"),
            ("Empower: ", ICY),
            ("Reduce cooldown; when activated, fires three frost arrows, each dealing "),
            (f"{player_projectiles['Bow_primary_enhanced'][0] * 100:.0f}% of ATK", ATK),
            (" damage and boosting the "),
            ("slowing", CC),
            (" effect to "),
            ("30%", SCALE),
            (".")
        ),
        Description(
            ("Ranger's Focus\n", WHITE, 28),
            ("Harness unwavering concentration and raise your bow, "),
            ("empowering", ICY),
            (" your Left Skill for "),
            (f"{skill_stats['Bow_secondary'][2] / 1000:.1f} seconds", TIME),
            (".")
        ),
        Description(
            ("Volley\n", WHITE, 28),
            ("Shoots nine cold-infused arrows, each dealing "),
            (f"{player_projectiles['Bow_q_skill'][0] * 100:.0f}% of ATK", ATK),
            (" and "),
            ("slowing", CC),
            (" enemies by "),
            ("60%", SCALE),
            (" for "),
            ("1 second", TIME),
            (".")
        ),
        Description(
            ("Enchanted Crystal Arrow\n", WHITE, 28),
            ("Sends forth an enormous crystalline arrow that penetrates barriers. It strikes the first foe for "),
            (f"{player_projectiles['Bow_e_skill'][0] * 100:.0f}% ATK damage", ATK),
            (" and "),
            ("stuns", CC),
            (" them for "),
            ("3 seconds", TIME),
            (", then detonates—enemies in the radius suffer "),
            (f"{aoe_stat['Bow_explosion'][0] * 100:.0f}% ATK damage", ATK),
            (" and are "),
            ("slowed", CC),
            (" by "),
            ("90%", SCALE),
            (" for "),
            ("5 seconds", TIME),
            (".")
        )
    ],
    "Bazooka" : [
        Description(),
        Description(),
        Description(),
        Description()
    ],
    "Lunar_gun" : [
        Description(
            ("Weapons of the Faithful\n", WHITE, 28),
            ("Calibrum: ", CALIBRUM),
            ("Fires a projectile that deals "),
            (f"{player_projectiles['Calibrum_primary'][0] * 100:.0f}% of ATK", ATK),
            (" damage to the enemy. If the enemy has a "),
            ("Calibrum Mark", CALIBRUM),
            (", it detonates the mark."),
            ('\n'),
            ("Infernum: ", INFERNUM),
            ("Fires a projectile that deals "),
            (f"{player_projectiles['Infernum_primary'][0] * 100:.0f}% of ATK", ATK),
            (" damage to the enemy and triggers "),
            ("Infernum Wave", INFERNUM),
            (".")
        ),
        Description(
            ("Lunar Swap\n", WHITE, 28),
            ("Flexible switch between "),
            ("Calibrum", CALIBRUM),
            (" and "),
            ("Infernum\n", INFERNUM),
            ("Skill special effects:\n", WHITE),
            ("Calibrum Mark: ", CALIBRUM),
            ("When detonated, deals "),
            (f"{apply_scale['Calibrum_mark'] * 100:.0f}% of ATK", ATK),
            (" as damage to the enemy and triggers "),
            ("Infernum Wave", INFERNUM),
            (", while also increasing movement speed by "),
            (f"30%", SCALE),
            (" for "),
            ("1 second", TIME),
            (".\n"),
            ("Infernum Wave: ", INFERNUM),
            ("Unleashes 4 piercing rays, each ray deals damage equal to "),
            (f"{player_projectiles['Infernum_ray'][0] * 100:.0f}% of ATK", ATK),
            (".")
        ),
        Description(
            ("Moonshot / Duskwave\n", WHITE, 28),
            ("Calibrum: ", CALIBRUM, 24),
            ("Fires a long-range shot that deals "),
            (f"{player_projectiles['Calibrum_skill'][0] * 100:.0f}% of ATK", ATK),
            (" to the first enemy hit and applies a "),
            ("Calibrum Mark", CALIBRUM),
            (" for "),
            ("5 seconds", TIME),
            (".\n"),
            ("Infernum: ", INFERNUM, 24),
            ("Unleashes a fiery wave made of three piercing flames, each dealing "),
            (f"{player_projectiles['Infernum_skill'][0] * 100:.0f}% of ATK", ATK),
            (". Enemies hit are marked with "),
            ("Calibrum Mark", CALIBRUM),
            (" for "),
            ("3 seconds", TIME),
            (".")
        ),
        Description(
            ("Moonlight Vigil\n", WHITE, 28),
            ("Fires a lunar spotlight forward, piercing terrain and exploding upon contact with an enemy. The explosion's effects vary based on the current lunar weapon:\n"),
            ("Calibrum: ", CALIBRUM, 24),
            ("Deals "),
            (f"{aoe_stat['Calibrum_ult'][0] * 100:.0f}% of ATK", ATK),
            (" damage and applies "),
            ("Calibrum Mark", CALIBRUM),
            (" to all affected enemies.\n"),
            ("Infernum: ", INFERNUM, 24),
            ("Deals "),
            (f"{aoe_stat['Infernum_ult'][0] * 100:.0f}% of ATK", ATK),
            (" damage and triggers 8 direction "),
            ("Infernum Ray", INFERNUM),
            (" on all hit enemies.\n"),
        )
    ]
}