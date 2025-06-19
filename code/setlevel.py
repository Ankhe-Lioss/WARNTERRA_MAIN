from weapon import *
from sprites import *
from player import *
from weapon import *
from spawn import *


def setlevel(game):
    game.room = -1
    
    game.map = load_pygame(os.path.join( 'data', 'maps', f'Level{game.level}.tmx'))
    game.spawnlist={
        #1=list[value=(obj.name,x,y)
    }
    game.checkins = {}
    game.doorlist = []
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
            game.player = Player((obj.x, obj.y), game)
            
            # Temporary weapon
            game.player.weap = Gauntlet(game)
        else:
            if 'room' in obj.properties:
                if obj.name == "Check_in":
                    game.checkins[obj.properties['room']] = (obj.x, obj.y)
                else:
                    if not obj.properties['room'] in game.spawnlist:
                        game.spawnlist[obj.properties['room']] = {}
                        
                    if not obj.properties['wave'] in game.spawnlist[obj.properties['room']]:
                            
                        #print(obj.properties['room'], obj.properties['wave'])
                        game.spawnlist[obj.properties['room']][obj.properties['wave']] = []
                    game.spawnlist[obj.properties['room']][obj.properties['wave']].append((obj.name, obj.x, obj.y))
    game.room_numb = len(game.spawnlist)
    print(game.room_numb)
    
    
def spawn_door(doorlist,game):
    for obj in doorlist:
        Door(obj[0], obj[1], (game.all_sprites, game.collision_sprites))

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
    if game.spawn_numb == 0:
        if game.room == game.room_numb:
            game.level += 1
            setlevel(game)
        game.room += 1
        spawn_room(game)
        game.wave = -1
    
    if game.spawn_numb == 1 and game.room > 0:
        if game.wave >= len(game.spawnlist[game.room]) - 1:
            pass
        else:
            game.wave += 1
            spawn_wave(game)

def check_game_state(game):
    print(game.wave)
    if game.state == "in_level":
        update_level(game)