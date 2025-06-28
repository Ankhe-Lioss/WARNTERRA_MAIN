from setting import *

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, user):
        super().__init__(user.game.all_sprites)
        self.user = user
        self.type = 'top'

        # Load bar images AFTER display is initialized
        self.bar_bg = user.game.bar_bg
        self.bar_empty = user.game.bar_empty
        self.bar_full = user.game.bar_full
        # Bar configuration
        self.width = 32
        self.height = 5
        self.offset_y =-5

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=user.rect.midtop)
        self.rect.y += self.offset_y
        self.image_rect = self.rect  # For compatibility with your custom draw()

        self.display_hp = self.user.hp
        self.hp_delay_speed = self.user.maxhp / 2  # adjust for red bar trailing



    def render_bar(self):
        self.image.fill((0, 0, 0, 0))  # clear

        # Calculate %s
        hp_ratio = max(0, min(1, self.user.hp / self.user.maxhp))
        delayed_ratio = max(0, min(1, self.display_hp / self.user.maxhp))

        green_width = int(1+30* hp_ratio)
        red_width = int(1+30 * delayed_ratio)
        # Background layer
        self.image.blit(self.bar_bg, (0, 0))
        # Red (delayed) layer
        if red_width > 0:
            red_bar = self.bar_empty.subsurface(pygame.Rect(0, 0, red_width, self.height)).copy()
            self.image.blit(red_bar, (0, 0))

        # Green layer
        if green_width > 0:
            green_bar = self.bar_full.subsurface(pygame.Rect(0, 0, green_width, self.height)).copy()
            self.image.blit(green_bar, (0, 0))
        
    def update(self, dt):
        if self.user.hp <= 0:
            self.kill()
            return

        # Smooth red bar decay
        if self.display_hp > self.user.hp:
            self.display_hp -= self.hp_delay_speed * dt
            if self.display_hp < self.user.hp:
                self.display_hp = self.user.hp
        elif self.display_hp < self.user.hp:
            self.display_hp = self.user.hp

        # Update position
        self.rect.midbottom = self.user.image_rect.midtop
        self.rect.y += self.offset_y

        # Re-render bar
        self.render_bar()


class Player_healthbar(pygame.sprite.Sprite):
    def __init__(self, user):
        self.user = user
        self.type = 'top'

        # Load bar images AFTER display is initialized
        self.bar_bg_frames=[]
        self.load_image()
        self.frame_index = 0
        self.bar_bg = self.bar_bg_frames[self.frame_index]
        self.bar_full =pygame.image.load(os.path.join('images','UI',"player_health_bar","5.png")).convert_alpha()
        # Bar configuration
        self.font=pygame.font.Font(os.path.join('images', 'font', 'DungeonChunk.ttf'), 20)
        self.level_font = pygame.font.Font(os.path.join('images', 'font', 'DungeonChunk.ttf'), 43)

        self.image = pygame.Surface((self.bar_bg.width, self.bar_bg.height), pygame.SRCALPHA)
    def load_image(self):
        for i in range(1,5):
            surf=pygame.image.load(os.path.join('images','UI',"player_health_bar",f"{i}.png")).convert_alpha()
            self.bar_bg_frames.append(surf)
    def render_bar(self):
        self.image.fill((0, 0, 0, 0))  # clear
        # Calculate %s
        hp_ratio = max(0, min(1, self.user.hp / self.user.maxhp))

        red_width = int(74 + 138 * hp_ratio)

        if red_width > 0:
            red_bar = self.bar_full.subsurface(pygame.Rect(0, 0, red_width,self.bar_bg.height)).copy()
            self.image.blit(red_bar, (0, 0))

        self.bar_bg=self.bar_bg_frames[int(self.frame_index % 4)]
        # Background layer
        self.image.blit(self.bar_bg, (0, 0))
        text=self.font.render(f"{int(self.user.hp)}/{int(self.user.maxhp)}", True, 'White')
        self.image.blit(text,(90,52))
        text=self.level_font.render(f"{int(self.user.game.level+1)}", True, 'White')
        self.image.blit(text,(28,36))
    def update(self, dt):
        if self.user.hp <= 0:
            self.kill()
            return

        # Smooth red bar decay

        # Update position
        self.frame_index += 6 * dt
        # Re-render bar
        self.render_bar()
        self.user.game.display_surface.blit(self.image, (0,600))