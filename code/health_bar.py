from setting import *
from entities import *

# Load health bar images
health_bar_image = []
for i in range(6):
    surf = pygame.image.load(os.path.join('images', 'UI', 'health_bar', f'{i}.png'))
    health_bar_image.append(surf)
class Healthbar(pygame.sprite.Sprite):
    def __init__(self, user):
        super().__init__(user.game.all_sprites)
        self.user = user
        self.image = health_bar_image[5]
        self.rect = self.image.get_rect(topleft=(user.rect.x + 10, user.rect.y - 10))

    def update(self,dt):
        self.rect.topleft = (self.user.rect.x + 10, self.user.rect.y - 10)
        health_percentage=self.user.hp / self.user.maxhp
        health_index = max(0, min(5, int(health_percentage * 5)))
        if self.user.hp <= 0:
            self.kill()
        self.image = health_bar_image[health_index]
