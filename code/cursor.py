import pygame
import os

def check_cursor(game):
    if pygame.joystick.get_count() > 0:
        game.joystick = pygame.joystick.Joystick(0)
        game.joystick.init()
        game.have_joystick = True
    else:
        game.have_joystick = False
    cursorxy=pygame.Vector2(pygame.mouse.get_pos())
    if not game.have_joystick:
        game.display_surface.blit(game.cursor_image, cursorxy + (-8, -8))
    if pygame.mouse.get_pressed()[1]:
        print(cursorxy)
