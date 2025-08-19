import pygame
from utils.suport import resize_image
from inputs.input_manager import InputManager
from utils.enums import InputType

class Dialog:
    def __init__(self, player, text: str, inputs: InputManager):
        self.display_surface = pygame.display.get_surface()

        self.player = player
        self.dialogs = text.split('*paragraph*')
        self.inputs = inputs

        self.dialogs_delay = pygame.time.get_ticks()
        self.selected_option = 0
        self.actual_text_size = 0

        self.button_clicked_time = pygame.time.get_ticks()
        self.display = False

    def set_dialogs(self, value: str):
        self.dialogs = value.split('*paragraph*')

        if value == '':
            self.display = False
        else:
            self.display = True

    def display_dialog(self):
        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() - 100

        overlay_surface = pygame.Surface((self.display_surface.get_width() // 2 - 100, 20 * len(self.dialogs) + 80), pygame.SRCALPHA)
        overlay_surface.fill((40, 40, 40))
        overlay_surface.set_alpha(230)

        overlay_rect = overlay_surface.get_rect(midbottom = (pos_x, pos_y))

        self.display_surface.blit(overlay_surface, overlay_rect)

        text_list = self.dialogs[self.selected_option][:self.actual_text_size].splitlines()

        for index, text in enumerate(text_list):
            dialog_font = pygame.font.Font(size=24)
            dialog_text_surface = dialog_font.render(text, True, (255, 255, 255))
            dialog_text_rect = dialog_text_surface.get_rect(midbottom = (pos_x, pos_y - 10 - (overlay_surface.get_height() // 2) + (index * (dialog_text_surface.get_height() + 5))))

            self.display_surface.blit(dialog_text_surface, dialog_text_rect)

        if self.actual_text_size < len(self.dialogs[self.selected_option]) - 1 and pygame.time.get_ticks() > self.dialogs_delay:
            self.actual_text_size += 1
            self.dialogs_delay = pygame.time.get_ticks() + 15
            self.check_inputs(True)

        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() - 64

        select_btn_font = pygame.font.Font(size=24)
        select_btn_text_surface = select_btn_font.render(
            "Avançar" if self.actual_text_size != len(self.dialogs[self.selected_option]) - 1 
                else "Continuar" if self.selected_option < len(self.dialogs) - 1 
                else "Terminar", 
            True, 
            (255, 255, 255)
        )
        select_btn_text_rect = select_btn_text_surface.get_rect(center = (pos_x, pos_y))

        select_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/{'scd_attack_button' if self.selected_option == len(self.dialogs) - 1 and len(self.dialogs[self.selected_option]) - 1 == self.actual_text_size else 'frst_attack_button'}/default.png', 1)
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
        if inputs.is_unpausing() and self.selected_option == len(self.dialogs) - 1 and now > self.button_clicked_time:
            self.set_dialogs('')
            self.player.interaction_button_pressed = False
            self.dialogs_delay = pygame.time.get_ticks()
            self.selected_option = 0
            self.actual_text_size = 0

            self.button_clicked_time = now + 300