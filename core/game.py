import pygame
from settings import *
from core.event import Event
from core.config import Config
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
        self.settings = Config() 
        
        if settings()['first_time']:
            level_type = LevelType.HISTORY
        else:
            level_type = LevelType.MAINMENU
        
        self.level = Level(level_type, self.settings)

    def run(self):
        while True:
            events = self.event.run()
            self.settings.run()
            
            self.screen.fill('black')

            self.level.run(events)

            pygame.display.update()
            self.clock.tick(FPS)