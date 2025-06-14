from setting import *
from entities import *

health_bar_full_image = pygame.image.load(os.path.join('images', 'UI', 'health_bar', '5.png'))
health_bar_empty_image = pygame.image.load(os.path.join('images', 'UI', 'health_bar', '0.png'))
class Healthbar():
    def __init__(self,user):
        Background_healthbar(user)
        Percentage_healthbar(user)

class Background_healthbar(pygame.sprite.Sprite):
    def __init__(self,user):
        super().__init__(user.game.all_sprites)
        self.user = user
        self.top_sprite = True  # This sprite is always on top
        self.image = health_bar_empty_image
        self.image_rect = self.image.get_rect(topleft=(user.rect.x + 10, user.rect.y - 10))
    def update(self, dt):
        if self.user.hp <= 0:
            self.kill()
            return
        self.image_rect.center = self.user.image_rect.midtop
        self.image_rect.x += 1
        #pygame.rect.FRect().



class Percentage_healthbar(pygame.sprite.Sprite):
    def __init__(self, user):
        super().__init__(user.game.all_sprites)
        self.user = user
        self.top_sprite = True
        self.original_image = health_bar_full_image  # Keep the original full bar image
        self.image = self.original_image.copy()  # Create an editable copy
        self.image_rect = self.image.get_rect(topleft=(user.rect.x + 10, user.rect.y - 10))

    def update(self, dt):
        if self.user.hp <= 0:
            self.kill()
            return

        # Update position
        self.image_rect.center = self.user.image_rect.midtop
        self.image_rect.x += 1

        # Calculate health percentage, clamped between 0 and 1
        health_percentage = max(0, min(1, self.user.hp / self.user.maxhp))

        # Calculate new width for the chopped health bar
        new_width = 1+int(30 * health_percentage)

        # Create a rectangle for the subsurface
        chopped_rect = pygame.Rect(0, 0, new_width, 5)

        # Extract subsurface safely
        self.image = self.original_image.subsurface(chopped_rect).copy()
