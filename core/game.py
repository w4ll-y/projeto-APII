import pygame
from settings import *
from core.event import Event
from levels.level import Level

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Event(self)
        
        self.level = Level()

    def run(self):
        while True:
            self.event.run()
            
            self.screen.fill('black')

            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)