import pygame
from settings import *
from core.entity import Entity

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Entity()

    def run(self):
        while True:
            self.event.run()

            self.screen.fill('black')

            pygame.display.update()
            self.clock.tick(FPS)
