import pygame
import time
from inputs.input_manager import InputManager
from utils.suport import reset_game, resize_image
from utils.enums import LevelType, InputType
from ui.menu.config import ConfigScreen

class MainMenu():
    def __init__(self, inputs: InputManager, level):
        self.inputs = inputs
        self.level = level

        self.display_surface = pygame.display.get_surface()

        self.options = ["Iniciar Jogo", "Ver História", "Configurações", "Sair do Jogo"]
        self.selected_option = 0

        self.button_clicked_time = pygame.time.get_ticks()

        self.config = ConfigScreen(self.inputs, self.level, [time.time() + 600], self)
        self.is_config_screen = False

    def display_menu(self):
        if self.is_config_screen:
            self.config.display_menu()
            return
        
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(256)

        self.display_surface.blit(overlay, (0, 0))

        #display buttons
        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() - 64

        select_btn_font = pygame.font.Font(size=24)
        select_btn_text_surface = select_btn_font.render("Selecionar", True, (255, 255, 255))
        select_btn_text_rect = select_btn_text_surface.get_rect(center = (pos_x, pos_y))

        select_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/frst_attack_button/default.png', 1)
        select_btn_rect = select_btn_graphic.get_rect(center= (pos_x - select_btn_text_surface.get_width(), pos_y))

        self.display_surface.blit(select_btn_graphic, select_btn_rect)
        self.display_surface.blit(select_btn_text_surface, select_btn_text_rect)

        for index, text in enumerate(self.options):
            font = pygame.font.Font(size=36)
            text_surface = font.render(text, True, (128, 128, 128) if index != self.selected_option else (255, 255, 255))

            pos_x = self.display_surface.get_width() // 2
            pos_y = self.display_surface.get_height() // 2 - ((-64) * (index - 1))

            text_rect = text_surface.get_rect(center = (pos_x, pos_y))

            self.display_surface.blit(text_surface, text_rect)

            self.check_inputs()

    def check_inputs(self):
        inputs = self.inputs.get_input()
        now = pygame.time.get_ticks()

        if inputs.is_walk_up() and self.selected_option > 0 and now > self.button_clicked_time:
            self.selected_option -= 1
            self.button_clicked_time = now + 300
        elif inputs.is_walk_down() and self.selected_option < len(self.options) - 1 and now > self.button_clicked_time:
            self.selected_option += 1
            self.button_clicked_time = now + 300
        elif inputs.is_selecting() and now > self.button_clicked_time:
            match self.selected_option:
                case 0:
                    reset_game()
                    self.level.reset(LevelType.OPENMAP, self.level.settings, [time.time() + 600])
                case 1:
                    self.level.reset(LevelType.HISTORY, self.level.settings, [time.time() + 600])
                case 2:
                    self.is_config_screen = True
                case 3:
                    reset_game()
                    exit()

            self.button_clicked_time = now + 300
            