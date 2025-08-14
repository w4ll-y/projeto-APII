import pygame
from settings import *
from core.event import Event
from levels.level import Level
from utils.enums import LevelType
from utils.suport import read_settings as settings

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Event(self)
        
        if settings()['first_time']:
            level_type = LevelType.HISTORY
        else:
            level_type = LevelType.MAINMENU
        
        self.level = Level(level_type)

    def run(self):
        while True:
            events = self.event.run()
            
            self.screen.fill('black')

            self.level.run(events)

            pygame.display.update()
            self.clock.tick(FPS)