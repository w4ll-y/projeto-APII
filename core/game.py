import pygame
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

        #sound
        main_sound = pygame.mixer.Sound('assets/music/02.mp3')
        main_sound.set_volume(0.9)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            events = self.event.run()
            
            self.screen.fill('black')

            self.level.run(events)

            pygame.display.update()
            self.clock.tick(FPS)