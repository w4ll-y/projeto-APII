import pygame
import sys
from settings import WIDTH, HEIGTH
from utils.suport import reset_game

class Event:
    def __init__(self, game):
        self.game = game

        self.full_screen = False
        self.window_w = WIDTH
        self.window_h = HEIGTH

    def run(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                reset_game()
                pygame.quit()
                sys.exit()

        return events

