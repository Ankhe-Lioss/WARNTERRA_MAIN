import pygame
from os.path import join

cursor_image = pygame.image.load(join('images', 'UI', 'cursor.png'))
def cursor(game):
    cursorxy=pygame.mouse.get_pos()
    game.display_surface.blit(cursor_image.convert_alpha(),cursorxy+(4,-12))