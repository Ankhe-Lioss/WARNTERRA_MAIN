from weapon import *
from sprites import *
from player import *
from weapon import *
from spawn import *
from UI import UI  # Make sure UI is imported

def setlevel(game):
    print("Setting Level", game.level)
    
    
    
    game.room = -1

    # Load TMX map
    game.map = load_pygame(os.path.join('data', 'maps', f'Level{game.level}.tmx'))

    # Initialize structures
    game.spawnlist = {}
    game.checkins = {}
    game.doorlist = []
    game.doors = set()

    # Ground and Walls
    for x, y, image in game.map.get_layer_by_name('Ground').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites, 'ground')

    for x, y, image in game.map.get_layer_by_name('Floor').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites, 'floor')

    for x, y, image in game.map.get_layer_by_name('Wall').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites, 'wall')

    # Collision Sprites
    for obj in game.map.get_layer_by_name('Objects'):
        CollisionSprite((obj.x, obj.y), obj.image, (game.all_sprites, game.collision_sprites))

    for obj in game.map.get_layer_by_name('Collisions'):
        CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), game.collision_sprites)

    for obj in game.map.get_layer_by_name('Door'):
        game.doorlist.append(((obj.x, obj.y), obj.image))

    for obj in game.map.get_layer_by_name('Entities'):
        if obj.name == 'Player':
            # Create new player
            game.player = Player((obj.x, obj.y), game)
            game.player.weap = Bow(game)
            
#                              /\
#                             /TH\
#                            /IS F\
#                           / KING \
#                          / WEAPON \
#                         /__________\
#                            |    |
#                            |    |                            
#                            |    |
#                            |    |
#                            |    |
#                            |    |
#                            |    |
#                            |____|


            # Reinitialize the UI with the new player
            game.ui = UI(game, game.player, game.display_surface)

        else:
            print("adding", obj)
            if 'room' in obj.properties:
                if obj.name == "Check_in":
                    game.checkins[obj.properties['room']] = (obj.x, obj.y)
                else:
                    room = obj.properties['room']
                    wave = obj.properties['wave']
                    game.spawnlist.setdefault(room, {})
                    game.spawnlist[room].setdefault(wave, [])
                    game.spawnlist[room][wave].append((obj.name, obj.x, obj.y))

    game.room_numb = len(game.checkins) - 1

def endlevel(game):#
    for group in [game.all_sprites, game.player_sprites, game.enemy_sprites, game.player_projectiles, game.enemy_projectiles, game.collision_sprites]:
        for sprite in group:
            sprite.kill()

    # Stat for levels

def spawn_door(game):
    for obj in game.doorlist:
        game.doors.add(Door(obj[0], obj[1], (game.all_sprites, game.collision_sprites)))
        
def open_door(game):
    for door in game.doors:
        door.kill()
        del door

def spawn_wave(game):
    for obj in game.spawnlist[game.room][game.wave]:
        spawn_animation((obj[1], obj[2]), game, obj[0])
        game.spawn_numb += 1
    
def spawn_room(game):
    #print("asi")
    spawn_animation(game.checkins[game.room], game, 'Check_in')
    game.spawn_numb = 1
    if game.room == 0:
        return
    
""" CHECK GAME STATE
    This function checks the game state and spawns enemies or doors as needed."""

def update_level(game):
    # BGM
    if not pygame.mixer.get_busy() and game.game_state == "in_game" and game.current_BGM is None:
        pygame.mixer.music.load(os.path.join("audio", "BGM", "normal.wav"))
        pygame.mixer.music.play(loops=-1)
        game.current_BGM = "normal.wav"
    
    if game.spawn_numb == 0:
        if game.room == game.room_numb:
            game.level += 1
            game.player.updstat()
            endlevel(game)
            setlevel(game)
            return
        game.room += 1
        
        spawn_room(game)
        if game.room > 0:
            spawn_door(game)
            
        game.wave = -1
    
    if game.spawn_numb == 1 and game.room > 0:
        if game.wave >= len(game.spawnlist[game.room]) - 1:
            open_door(game)
        else:
            game.wave += 1
            spawn_wave(game)

def check_game_state(game):
    #print(game.wave)
    if game.state == "in_level":
        update_level(game)