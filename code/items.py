from setting import *
from weapon import *

class Item(pygame.sprite.Sprite):
    def __init__(self, game, image, pos=(0, 0)):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = image  # image must be provided by subclass
        self.base_pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)
        self.image_rect = self.rect.copy()
        self.collected = False
        self.updown = 0

    def apply_effect(self, player):
        pass

    def update(self, dt):
        # Bobbing effect
        self.updown += dt * 10
        offset = int(self.updown % 20)
        self.rect.center = (self.base_pos.x, self.base_pos.y + offset)
        self.image_rect.center=self.rect.center
        if not self.collected and self.rect.colliderect(self.game.player.rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.apply_effect(self.game.player)
                self.collected = True
                self.kill()



class Weapon_Item(Item):
    def __init__(self, pos, game, name):
        self.game = game
        self.name = name

        # Load and scale image
        surf = pygame.image.load(os.path.join('images', 'weapon', f'{self.name}.png')).convert_alpha()
        original_width, original_height = surf.get_size()
        scale_ratio = min(48 / original_width, 48 / original_height)
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        icon = pygame.transform.smoothscale(surf, (new_width, new_height))

        super().__init__(game, icon, pos)

    def apply_effect(self, player):
        weapon_class = Weapon_Dict.get(self.name)
        if weapon_class:
            player.weapons.append(weapon_class(self.game))
            player.current_weapon_index=len(player.weapons)-1
            player.weap=player.weapons[player.current_weapon_index]
            self.game.player_currweapdict.append(self.name)
            if self.name=="Bow" or self.name=="Gauntlet":
                for sprite in self.game.all_sprites:
                    if isinstance(sprite, Weapon_Item):
                        sprite.kill()