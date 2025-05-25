import pygame
import sys
from levels.level import Level

class Events:
    def __init__(self, game):
        self.game = game

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                width, heigth = event.w, event.h

                self.game.screen = pygame.display.set_mode((width, heigth), pygame.RESIZABLE)
                self.game.level.visible_sprites.save_window_size()

