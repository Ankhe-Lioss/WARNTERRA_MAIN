from weapon import *
from sprites import *
from player import *
from spawn import *
from UI import UI  # Make sure UI is imported
from items import *
def setlevel(game):
    level = game.level%5+1
    
    
    game.room = -1

    # Load TMX map
    game.map = load_pygame(os.path.join('data', 'maps', f'Example.tmx'))

    # Initialize structures
    game.spawnlist = {}
    game.checkins = {}
    game.doorlist = []
    game.doors = set()
    
    game.door_opened = True
    game.blessing_list = [None] * 5

    # Ground and Walls
#    for x, y, image in game.map.get_layer_by_name('Ground').tiles():
 #       Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites, 'ground')


    #Tile layer
    for x, y, image in game.map.get_layer_by_name('Floor').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites, 'ground')

    for x, y, image in game.map.get_layer_by_name('Wall').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites)

    for x, y, gid in game.map.get_layer_by_name('Animated Floor').iter_data():
        props = game.map.get_tile_properties_by_gid(gid)
        if props and 'type' in props:
            Animated_Ground((x * TILE_SIZE, y * TILE_SIZE),game ,props['type'])
    for x, y, image in game.map.get_layer_by_name('Decorative').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites)


    # Collision Sprites
#    for obj in game.map.get_layer_by_name('Objects'):
#        CollisionSprite((obj.x, obj.y), obj.image, (game.all_sprites, game.collision_sprites))
    #object layer
    for obj in game.map.get_layer_by_name('Non_animated_non_collision'):
        CollisionSprite((x * TILE_SIZE, y * TILE_SIZE), obj.image, game.all_sprites,None)

    for obj in game.map.get_layer_by_name('Non_animated_collision'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        CollisionSprite((obj.x, obj.y), obj.image, (game.all_sprites, game.collision_sprites),tile['type'],)

    for obj in game.map.get_layer_by_name('Animated_collision'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        Aninmated_Object((obj.x, obj.y), tile['type'], (game.all_sprites, game.collision_sprites),game)




    for obj in game.map.get_layer_by_name('Trap'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        Trap((obj.x, obj.y),game, tile['type'])


    for obj in game.map.get_layer_by_name('Animated_non_collision'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        Aninmated_Object((obj.x, obj.y), tile['type'], game.all_sprites, game)




    for obj in game.map.get_layer_by_name('Collisions'):
        CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), game.collision_sprites)

    for obj in game.map.get_layer_by_name('Door'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        Door((obj.x, obj.y),game, tile['type'])
    for obj in game.map.get_layer_by_name('Interactive'):
        tile = game.map.get_tile_properties_by_gid(obj.gid)
        if tile['type'] =='Explosive_Barrel':
            Explosive_Barrel((obj.x, obj.y),game)

    for obj in game.map.get_layer_by_name('Entities'):
        if obj.name == 'Player':
            # Create new player
            game.player = Player((obj.x, obj.y), game)
            # Give both weapons
            for weap in game.player_currweapdict:
                game.player.weapons.append(Weapon_Dict[weap](game))
                game.player.current_weapon_index = len(game.player.weapons)-1
                game.player.weap = game.player.weapons[game.player.current_weapon_index]
            # Reinitialize the UI with the new player
            game.ui = UI(game, game.player, game.display_surface)

        elif obj.name == 'Blessing':
            game.blessing_list[int(obj.type)] = (obj.x, obj.y)
        else:
            if 'room' in obj.properties:
                if obj.name == "Check_in":
                    game.checkins[obj.properties['room']] = (obj.x, obj.y)
                else:
                    room = obj.properties['room']
                    wave = obj.properties['wave']
                    game.spawnlist.setdefault(room, {})
                    game.spawnlist[room].setdefault(wave, [])
                    game.spawnlist[room][wave].append((obj.name, obj.x, obj.y))
            if obj.name == "Weapon" and len(game.player_currweapdict)==0:
                Weapon_Item((obj.x, obj.y), game, obj.type)

    game.room_numb = len(game.checkins) - 1
    game.map_layout= build_grid_from_sprites(game.map,game.collision_sprites)
    
def endlevel(game):
    for group in [game.all_sprites, game.player_sprites, game.enemy_sprites, game.player_projectiles, game.enemy_projectiles, game.collision_sprites]:
        for sprite in group:
            sprite.kill()

    # Stat for levels

def spawn_door(game):
    if not game.door_opened:
        return
    for door in game.door_sprites:
        door.toggle()
        game.door_opened = False
        
def open_door(game):
    if game.door_opened:
        return
    for door in game.door_sprites:
        door.toggle()
        game.door_opened = True

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
    
    if game.current_BGM == "start_menu":
        pygame.mixer.music.stop()
        game.current_BGM = None
        
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
        spawn_door(game)
            
        game.wave = -1
    
    if game.room == 0 and hasattr(game.player, 'weap') and game.player.weap is not None:
        open_door(game)
    
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
        
def build_grid_from_sprites(map,collision_sprites):
    grid = []
    #sdhuyghuihg isdhighsighdfsiughsd hgsdf hgsidufhsdiou hdohsidhdifuo iudfohiuo 
    tile_w = 32
    tile_h = 32
    map_w = map.width
    map_h = map.height
    for y in range(map_h):
        row = []
        for x in range(map_w):
            tile_rect = pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h)
            # Check if this tile collides with any collision sprite
            if any(sprite.rect.colliderect(tile_rect) for sprite in collision_sprites):
                row.append(1)  # blocked
            else:
                row.append(0)  # walkable
        grid.append(row)
        #print(row)
    return grid
