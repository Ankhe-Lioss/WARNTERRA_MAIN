from weapon import *
from sprites import *
from player import *
from weapon import *
from spawn import *



def setlevel(game):
    #
    #
    game.level=0
    map = load_pygame(os.path.join( 'data', 'maps', 'Level0.tmx'))
    game.spawnlist={
        #1=list[value=(obj.name,x,y)
    }
    for x, y, image in map.get_layer_by_name('Tile Layer 1').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites)
    for x, y, image in map.get_layer_by_name('Tile Layer 2').tiles():
        Ground((x * TILE_SIZE, y * TILE_SIZE), image, game.all_sprites)
    for obj in map.get_layer_by_name('Objects'):
        CollisionSprite((obj.x, obj.y), obj.image, (game.all_sprites, game.collision_sprites))

    for obj in map.get_layer_by_name('Collisions'):
        CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), game.collision_sprites)

    for obj in map.get_layer_by_name('Entities'):
        if obj.name == 'Player':
            game.player = Player((obj.x, obj.y), game)
            game.player.weap = Bow(game)
        else:
            if not obj.type in game.spawnlist:
                game.spawnlist[obj.type] = []
            game.spawnlist[obj.type].append((obj.name, obj.x, obj.y))
            
def spawn_enmey_wave(wave,game):
    for obj in game.spawnlist[f'{wave}']:
        spawn_animation((obj[1], obj[2]), game, obj[0])
        game.spawn_numb+=1