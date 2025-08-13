import pygame
import time
from settings import *
from core.event import Event
from levels.level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Event(self)
        
        self.level = Level()

        self.finish_game_time = time.time() + 600

    def run(self):
        while True:
            events = self.event.run()
            
            self.screen.fill('black')

            self.level.run(events, self.finish_game_time)

            pygame.display.update()
            self.clock.tick(FPS)