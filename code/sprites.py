from setting import *
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
'Armored_Table':((0,-32),(0,8))
}
class Ground(pygame.sprite.Sprite):
    """ Background map """

    def __init__(self, pos, surf, groups, type=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.type = type

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


class Aninmated_Object(pygame.sprite.Sprite):

    def __init__(self, pos, name,groups,game):
        super().__init__(groups)
        self.game = game
        self.name = name
        self.frames = self.game.animated_object_frames[self.name]
        self.image=self.frames[0]
        self.image_rect = self.image.get_frect(topleft=pos)
        inflate, offset = animated_image_offset.get(self.name, ((0, 0), (0, 0)))

        self.rect = self.image_rect.copy()
        self.rect = self.rect.inflate(*inflate)
        self.rect.topleft = (self.rect.left + offset[0], self.rect.top + offset[1])
    def update(self, dt):
        self.frame_index=self.game.frame_index
        self.image=self.frames[int(self.frame_index % len(self.frames))]

class Aninmated_Object(pygame.sprite.Sprite):

    def __init__(self, pos, name,groups,game):
        super().__init__(groups)
        self.game = game
        self.name = name
        self.frames = self.game.animated_object_frames[self.name]
        self.image=self.frames[0]
        self.image_rect = self.image.get_frect(topleft=pos)
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

    def update(self, dt):
        cycle_frame = int(self.game.frame_index % self.total_frames)

        # Decide state based on time slice
        if cycle_frame < self.off_frames:
            self.state = 'off'
            frame_list = self.frames['off']
            local_frame = cycle_frame
        else:
            self.state = 'on'
            frame_list = self.frames['on']
            local_frame = cycle_frame - self.off_frames

        # Animate current frame
        self.image = frame_list[local_frame % len(frame_list)]


class Animated_Ground(pygame.sprite.Sprite):
    """Animated ground tile (e.g. animated water)."""

    def __init__(self, pos, game,name):
        super().__init__(game.all_sprites)
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