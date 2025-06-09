from setting import *
from main import *
from weapon import *
from sprites import *
from player import Player

def setlevel(game):
    game.level = 0
    map = load_pygame(os.path.join( 'data', 'maps', 'Test_level.tmx'))
    
    # Loading map
    
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
            game.player = Player((obj.x, obj.y), game.all_sprites, game)
            print(game.player.rect)
            print(game.player.hitbox_rect)
            game.player.weap = Gauntlet(game.all_sprites, game)
        else:
            #Spawn_animation((obj.x, obj.y), game.all_sprites,game,obj.name)
            pass