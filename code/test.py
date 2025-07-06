import pygame
import os

pygame.mixer.init()

sound = pygame.mixer.music.load(os.path.join("audio", "test_folder", "0015.ogg"))
sound.play()