import pygame
import time
from settings import *
from core.event import Event
from levels.level import Level
from utils.enums import LevelType

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.event = Event(self)
        
        #O tempo para finalizar o jogo é salvo em uma lista porque, quando uma lista é passada
        #como parâmetro, eu posso alterar o valor original em outra parte do código.
        #Uma variável comum, quando passada como parâmetro, altera uma cópia criada para aquela parte do código, o valor original nâo é alterado
        self.level = Level(LevelType.MAINMENU)

    def run(self):
        while True:
            events = self.event.run()
            
            self.screen.fill('black')

            self.level.run(events)

            pygame.display.update()
            self.clock.tick(FPS)