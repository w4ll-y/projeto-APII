import pygame
from settings import *
from core.events import Events
from levels.level import Level
from utils.enums import LevelType

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Events()
        
        self.level = Level()

    def run(self):
        while True:
            self.event.run()
            
            self.screen.fill('black')

            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)
