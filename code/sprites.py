from setting import *
from aoe import *

#customizing hitbox rectangle and displaying rectangle
from status import Burning, Rooted

animated_image_offset={#name = (inflate,offset)
'Fountain':((0,-35),(0,10)),
'Broken_Pillar_Torch': ((-32,-78),(0,15)),
'Orb':((-96,-102),(0,38)),
'Torch_2': ((-82,-103),(0,0)),
'Magic_Stone': ((-64,-128),(0,32)),
'Haunted_Piano': ((-145,-150),(0,40)),
'Bookshelf':((-4,-24),(0,10)),
'Rock':((0,-16),(0,8)),
'Statues':((0,-42),(0,21)),
'Flames_trap':((0,-86),(0,43)),
'Pillar_Torch':((-32,-70),(0,35)),
'Wooden_Door':((0,-32),(0,-16)),
'Stone_Door':((0,-32),(0,-16)),
'Armored_Table':((0,-32),(0,8)),
'Shrine':((0,-52),(0,26)),
'Well':((0,-42),(0,21))
}
#the lowest floor of game that have the highest priortity in drawing so it alway behind every other object
class Ground(pygame.sprite.Sprite):
    """ Background map """

    def __init__(self, pos, surf, groups, type=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.type = type
#collision the invisible layer that resemble wall
class CollisionSprite(pygame.sprite.Sprite):
    
    """ Objects and walls """
    
    def __init__(self, pos, surf, groups,name=None,type=None):
        super().__init__(groups)
        self.image = surf
        self.image_rect = self.image.get_rect(topleft=pos)
        self.rect = self.image.get_rect(topleft=pos)
        if name:
            inflate, offset = animated_image_offset.get(name, ((0, 0), (0, 0)))
            self.rect = self.rect.inflate(*inflate)
            self.rect.topleft = (self.rect.left + offset[0], self.rect.top + offset[1])
#Check if the player have reached a certain point
class Check_in(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = game.check_in_image
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_frect(topleft=pos)
        self.visible = True
        
    def update(self, dt):
        if pygame.sprite.spritecollide(self, self.game.player_sprites,False):
            self.kill()
            self.game.spawn_numb -= 1

#Animated_Object to decorated and centurized the game play around something
class Aninmated_Object(pygame.sprite.Sprite):

    def __init__(self, pos, name,groups,game):
        super().__init__(groups)
        self.game = game
        self.name = name
        #load graphic
        self.frames = self.game.animated_object_frames[self.name]
        self.image=self.frames[0]
        self.image_rect = self.image.get_frect(topleft=pos)

        #custom self_hitbox
        inflate, offset = animated_image_offset.get(self.name, ((0, 0), (0, 0)))
        self.rect = self.image_rect.copy()
        self.rect = self.rect.inflate(*inflate)
        self.rect.topleft = (self.rect.left + offset[0], self.rect.top + offset[1])
        
    def update(self, dt):
        self.frame_index=self.game.frame_index
        self.image=self.frames[int(self.frame_index % len(self.frames))]


Trap_on_off_time={#Trap name:(frames number,off frames number,on frames number)
'Spikes':(14,5,9),
'Flames_trap':(12,4,8)
}
Trap_on_off_time = {
    # name: (total_frames, off_frames, on_frames)
    'Spikes': (14, 5, 9),
    'Flames_trap': (12, 4, 8)
}
#Trap with on/off state that have special effect on player if hit
class Trap(pygame.sprite.Sprite):
    def __init__(self, pos, game, name):
        super().__init__(game.all_sprites)
        self.game = game
        self.name = name
        self.frames = {'off': [], 'on': []}
        self.frame_index = 0

        self.total_frames, self.off_frames, self.on_frames = Trap_on_off_time[self.name]
        self.load_images()

        self.state = 'off' if self.frames['off'] else 'on'
        self.image = self.frames[self.state][0]
        self.image_rect = self.image.get_frect(topleft=pos)

        inflate, offset = animated_image_offset.get(self.name, ((0, 0), (0, 0)))
        self.rect = self.image_rect.copy()
        self.rect = self.rect.inflate(*inflate)
        self.rect.topleft = (self.rect.left + offset[0], self.rect.top + offset[1])

        # Cooldown values
        self.hit_cooldown = 0 # current timer
        self.hit_delay = 2000

    def load_images(self):
        base_path = os.path.join('images', 'traps', self.name)
        for state in ['off', 'on']:
            state_path = os.path.join(base_path, state)
            for i in range(1, 100):
                img_path = os.path.join(state_path, f"{i}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                    self.frames[state].append(img)
                else:
                    break
    #check if collide with player while on and no cooldown
    def collision_with_player(self):
        if self.state == 'on' and self.hit_cooldown == 0:
            if self.rect.colliderect(self.game.player.rect):
                self.hit_cooldown = self.hit_delay
                if self.name=='Flames_trap':
                    pass
                if self.name=='Spikes':
                    pass
    def update(self, dt):
        # Decrease cooldown using dt
        if self.hit_cooldown > 0:
            self.hit_cooldown -=1000*dt
            if self.hit_cooldown < 0:
                self.hit_cooldown = 0

        # Frame animation logic
        cycle_frame = int(self.game.frame_index % self.total_frames)

        if cycle_frame < self.off_frames:
            self.state = 'off'
            frame_list = self.frames['off']
            local_frame = cycle_frame
        else:
            self.state = 'on'
            frame_list = self.frames['on']
            local_frame = cycle_frame - self.off_frames

        self.image = frame_list[local_frame % len(frame_list)]

        # Check for player collision if trap is active
        self.collision_with_player()

    def collision_with_player(self):
        if self.state == 'on' and self.hit_cooldown == 0:
            if self.rect.colliderect(self.game.player.rect):
                self.hit_cooldown = self.hit_delay
                if self.name=='Flames_trap':
                    Burning(2000, self.game.player.maxhp * 0.05, self.game, self.game.player)
                if self.name=='Spikes':
                    self.game.player.take_damage(self.game.player.maxhp * 0.05)

#Animated ground layer with special effect
class Animated_Ground(pygame.sprite.Sprite):
    """Animated ground tile (e.g. animated water)."""

    def __init__(self, pos, game,name):
        super().__init__(game.all_sprites,game.animated_tiles)
        self.game = game
        self.name = name
        self.frames=[]
        self.ground_type = self.name.split('_')[0]
        self.load_image()
        self.image=self.frames[0]
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.type = 'floor'


    def load_image(self):
        base_path = os.path.join('images', 'animated_tiles', self.ground_type, self.name)

        if not os.path.exists(base_path):
            print(f"[ERROR] Path does not exist: {base_path}")
            return

        for i in range(1, 100):  # Supports up to 99 frames
            file_path = os.path.join(base_path, f"{i}.png")
            if os.path.exists(file_path):
                img = pygame.image.load(file_path).convert_alpha()
                self.frames.append(img)
            else:
                break  # Stop loading if a frame is missing

        if not self.frames:
            print(f"[WARNING] No frames found in: {base_path}")
    def update(self, dt):
        self.frame_index=self.game.frame_index
        self.image=self.frames[int(self.frame_index % len(self.frames))]
#Door to open and close for game intend experience
class Door(pygame.sprite.Sprite):
    def __init__(self, pos, game, name):
        super().__init__(game.all_sprites,game.door_sprites)
        self.game = game
        self.name = name
        self.pos = pos
        self.state = 'opening'
        self.frame_index = 0
        self.frames = {
            'opening': [],
            'opened': [],
            'closing': [],
            'closed': []
        }
  # Adjust as needed
        self.load_images()

        self.image = self.frames[self.state][0]
        self.image_rect = self.image.get_rect(topleft=pos)
        inflate, offset = animated_image_offset.get(self.name, ((0, 0), (0, 0)))
        self.rect = self.image_rect.copy()
        self.rect = self.rect.inflate(*inflate)
        self.rect.topleft = (self.rect.left + offset[0], self.rect.top + offset[1])

    def load_images(self):
        base_path = os.path.join('images', 'Door', self.name)

        for state in self.frames:
            state_path = os.path.join(base_path, state.capitalize())
            if not os.path.exists(state_path):
                continue

            i = 1
            while True:
                img_path = os.path.join(state_path, f"{i}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                    self.frames[state].append(img)
                    i += 1
                else:
                    break

    def toggle(self):
        if self.state in ['closed', 'closing']:
            self.state = 'opening'
            self.frame_index = 0
        elif self.state in ['opened', 'opening']:
            self.state = 'closing'
            self.frame_index = 0

    def update(self, dt):
        if self.state in ['opening', 'closing']:
            self.frame_index += 6*dt
            frame_list = self.frames[self.state]

            if self.frame_index >= len(frame_list):
                # Transition to final state
                if self.state == 'opening':
                    self.state = 'opened'
                    self.remove(self.game.collision_sprites)
                else:
                    self.state = 'closed'
                    self.add(self.game.collision_sprites)

                self.frame_index = 0

            self.image = self.frames[self.state][int(self.frame_index)]

        else:
            # Ensure collision group reflects the current state
            if self.state == 'closed':
                self.add(self.game.collision_sprites)
            else:
                self.remove(self.game.collision_sprites)

            self.image = self.frames[self.state][0]
#Explosive barrel for game
class Explosive_Barrel(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        super().__init__(game.all_sprites, game.collision_sprites)
        self.game = game
        self.pos = pos
        self.state = 'idle'
        self.warning_timer = 0
        self.warning_duration = 1.0  # 1 second
        self.frame_index = 0

        # Load animation frames
        self.frames = []
        self.load_images()

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos).inflate(-108,-100)
        self.image_rect = self.image.get_rect(topleft=pos)
    def load_images(self):
        path = os.path.join('images', 'barrel', 'Explosive')
        i = 1
        while True:
            img_path = os.path.join(path, f"{i}.png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                self.frames.append(img)
                i += 1
            else:
                break

    def update(self, dt):
        if self.state == 'idle':
            if pygame.sprite.spritecollideany(self, self.game.aoe_sprites):
                #print('ocj')
                self.state = 'warning'
                self.warning_timer = 0
                self.frame_index = 0

        elif self.state == 'warning':
            self.warning_timer += dt

            # Loop the animation frames during
            self.frame_index += 6 * dt
            self.image = self.frames[int(self.frame_index)%len(self.frames)]

            if self.warning_timer >= self.warning_duration:
                self.explode()

    def explode(self):
        Barrel_Explode(self.rect.center, self.game)
        self.kill()
