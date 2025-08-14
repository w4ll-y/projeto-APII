import pygame
from inputs.input_manager import InputManager

class Pause():
    def __init__(self, inputs: InputManager, player):
        self.inputs = inputs
        self.player = player

        self.display_surface = pygame.display.get_surface()

        self.options = ["Continue", "Reiniciar", "Sair para o Menu"]
        self.selected_option = 0

        self.button_clicked_time = pygame.time.get_ticks()

    def display_menu(self):
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120)

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

            self.button_clicked_time = now + 300
            