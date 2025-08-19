import pygame
import time
from inputs.input_manager import InputManager
from utils.suport import reset_game, resize_image, change_settings_value
from utils.enums import LevelType, InputType
from utils.assets import GAME_HISTORY

class History():
    def __init__(self, inputs: InputManager, level):
        self.inputs = inputs
        self.level = level

        self.display_surface = pygame.display.get_surface()

        self.dialogs = GAME_HISTORY.split('*paragraph*')
        self.dialogs_delay = pygame.time.get_ticks()
        self.selected_option = 0
        self.actual_text_size = 0

        self.button_clicked_time = pygame.time.get_ticks()

    def display_text(self):        
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((33, 33, 33))
        overlay.set_alpha(256)

        self.display_surface.blit(overlay, (0, 0))

        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() // 2

        text_list = self.dialogs[self.selected_option][:self.actual_text_size].splitlines()

        for index, text in enumerate(text_list):
            dialog_font = pygame.font.Font(size=24)
            dialog_text_surface = dialog_font.render(text, True, (255, 255, 255))
            dialog_text_rect = dialog_text_surface.get_rect(center = (pos_x, pos_y + 50 + (dialog_text_surface.get_height() * (index - len(text_list) / 2))))

            self.display_surface.blit(dialog_text_surface, dialog_text_rect)

        if self.actual_text_size < len(self.dialogs[self.selected_option]) - 1 and pygame.time.get_ticks() > self.dialogs_delay:
            self.actual_text_size += 1
            self.dialogs_delay = pygame.time.get_ticks() + 15
            self.check_inputs(True)
        elif self.actual_text_size == len(self.dialogs[self.selected_option]) - 1:
            #display buttons
            pos_x = self.display_surface.get_width() // 2
            pos_y = self.display_surface.get_height() - 64

            select_btn_font = pygame.font.Font(size=24)
            select_btn_text_surface = select_btn_font.render("Continuar" if self.selected_option < len(self.dialogs) - 1 else "Terminar", True, (255, 255, 255))
            select_btn_text_rect = select_btn_text_surface.get_rect(center = (pos_x, pos_y))

            select_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/frst_attack_button/default.png', 1)
            select_btn_rect = select_btn_graphic.get_rect(center= (pos_x - select_btn_text_surface.get_width(), pos_y))

            self.display_surface.blit(select_btn_graphic, select_btn_rect)
            self.display_surface.blit(select_btn_text_surface, select_btn_text_rect)

            self.check_inputs()

    def check_inputs(self, pre_finish = False):
        inputs = self.inputs.get_input()
        now = pygame.time.get_ticks()

        if pre_finish and inputs.is_selecting() and now > self.button_clicked_time:
            self.actual_text_size = len(self.dialogs[self.selected_option]) - 1
            self.button_clicked_time = pygame.time.get_ticks() + 500
            return

        if inputs.is_selecting() and now > self.button_clicked_time:
            if self.selected_option < len(self.dialogs) - 1:
                self.selected_option += 1
                self.actual_text_size = 0
                self.button_clicked_time = pygame.time.get_ticks() + 500
                self.display_text()
            else:
                reset_game()
                change_settings_value('first_time', False)
                self.level.reset(LevelType.MAINMENU, self.level.settings, [time.time() + 600])

            self.button_clicked_time = now + 300