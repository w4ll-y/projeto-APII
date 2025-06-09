import pygame
import sys
from settings import WIDTH, HEIGTH

class Event:
    def __init__(self, game):
        self.game = game

        self.full_screen = False
        self.window_w = WIDTH
        self.window_h = HEIGTH

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                width, heigth = event.w, event.h

                self.game.screen = pygame.display.set_mode((width, heigth), pygame.RESIZABLE)

                if self.full_screen:
                    self.game.screen = pygame.display.set_mode((self.window_w, self.window_h), pygame.RESIZABLE)
                    self.full_screen = False

                self.game.level.visible_sprites.save_window_size()


            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_F11:
                        if not self.full_screen:
                            self.window_w, self.window_h = self.game.screen.get_size()

                            self.game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.full_screen = True
                        else:
                            self.game.screen = pygame.display.set_mode((self.window_w, self.window_h))
                        
                        self.game.level.visible_sprites.save_window_size()

