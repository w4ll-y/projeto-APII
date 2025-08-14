import pygame
import time
from inputs.input_manager import InputManager
from utils.suport import reset_game
from utils.enums import LevelType

class Pause():
    def __init__(self, inputs: InputManager, level, finish_game_time):
        self.inputs = inputs
        self.player = None
        self.level = level
        self.finish_game_time = finish_game_time

        self.display_surface = pygame.display.get_surface()

        self.options = ["Continue", "Reiniciar", "Sair para o Menu"]
        self.selected_option = 0

        self.button_clicked_time = pygame.time.get_ticks()
        
        self.reset_game = False

    def set_player(self, player):
        self.player = player

    def display_menu(self):
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120 if not self.reset_game else 256)

        self.display_surface.blit(overlay, (0, 0))

        for index, text in enumerate(self.options):
            font = pygame.font.Font(size=36)
            text_surface = font.render(text, True, (255, 255, 255) if index != self.selected_option else (128, 128, 128))

            pos_x = self.display_surface.get_width() // 2
            pos_y = self.display_surface.get_height() // 2 - ((-64) * (index - 1))

            text_rect = text_surface.get_rect(center = (pos_x, pos_y))

            self.display_surface.blit(text_surface, text_rect)

            self.check_inputs()

    def check_inputs(self):
        inputs = self.inputs.get_input()
        now = pygame.time.get_ticks()

        if inputs.is_unpausing() and now > self.button_clicked_time:
            self.player.paused_game = False
            self.button_clicked_time = now + 300
        elif inputs.is_walk_up() and self.selected_option > 0 and now > self.button_clicked_time:
            self.selected_option -= 1
            self.button_clicked_time = now + 300
        elif inputs.is_walk_down() and self.selected_option < len(self.options) - 1 and now > self.button_clicked_time:
            self.selected_option += 1
            self.button_clicked_time = now + 300
        elif inputs.is_selecting() and now > self.button_clicked_time:
            match self.selected_option:
                case 0:
                    self.player.paused_game = False
                case 1:
                    self.reset_game = True
                    self.finish_game_time[0] = time.time() + 600
                    reset_game()
                    self.level.reset(LevelType.OPENMAP, self.finish_game_time)
                case 2:
                    self.reset_game = True
                    reset_game()
                    self.level.reset(LevelType.MAINMENU, self.finish_game_time)

            self.button_clicked_time = now + 300
            