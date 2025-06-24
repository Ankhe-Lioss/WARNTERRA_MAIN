import pygame
import os
from random import *
from math import *
from data import *
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 200
TILE_SIZE = 32
CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
def inflate_custom(rect, left=0, top=0, right=0, bottom=0):
    return pygame.Rect(
        rect.left - left,
        rect.top - top,
        rect.width + left + right,
        rect.height + top + bottom
    )