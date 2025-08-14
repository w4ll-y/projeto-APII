import pygame
import time
from inputs.input_manager import InputManager
from utils.suport import reset_game, resize_image, read_settings, change_settings_value, read_json
from utils.enums import LevelType, InputType

class Config():
    def __init__(self, inputs: InputManager, level, finish_game_time, pre_screen):
        self.inputs = inputs
        self.level = level
        self.finish_game_time = finish_game_time
        self.pre_screen = pre_screen

        self.display_surface = pygame.display.get_surface()

        self.settings = read_settings()
        self.settings_options = read_json("data/settings_options.json")

        self.options = {
            "fullscreen_mode": "Tela Cheia",
            "window_size": "Tamanho da Janela",
            "music_volume": "Volume da Música",
            "play_music": "Tocar Música",
            "difficult": "Dificuldade"
        }
        self.selected_option = list(self.options.keys())[0]

        self.button_clicked_time = pygame.time.get_ticks()

        self.saved_time = 0

    def display_menu(self):
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(256 if not self.pre_screen == LevelType.MAINMENU else 120)

        self.display_surface.blit(overlay, (0, 0))

        self.display_saved_text()
        self.display_buttons()

        i = 0

        for key, value in self.options.items():
            font = pygame.font.Font(size=36)
            text_surface = font.render(value, True, (255, 255, 255) if key != self.selected_option else (128, 128, 128))

            pos_x = self.display_surface.get_width() // 2 - 100
            pos_y = self.display_surface.get_height() // 2  + 50 + (text_surface.get_height() * (i - len(self.options.keys()) / 2))

            text_rect = text_surface.get_rect(midright = (pos_x, pos_y))

            val = self.settings[key]

            value_font = pygame.font.Font(size=36)
            value_text_surface = value_font.render(self.format_values(val), True, (255, 255, 255) if key != self.selected_option else (128, 128, 128))
            value_text_rect = text_surface.get_rect(midleft = (pos_x + 200, pos_y))

            self.display_surface.blit(text_surface, text_rect)
            self.display_surface.blit(value_text_surface, value_text_rect)

            self.check_inputs()

            i += 1

    def display_buttons(self):
        #display buttons
        pos_x = self.display_surface.get_width() // 2 - 100
        pos_y = self.display_surface.get_height() - 64

        select_btn_font = pygame.font.Font(size=24)
        select_btn_text_surface = select_btn_font.render("<- -> Mudar Valor", True, (255, 255, 255))
        select_btn_text_rect = select_btn_text_surface.get_rect(midright = (pos_x, pos_y))

        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() - 64

        confirm_btn_font = pygame.font.Font(size=24)
        confirm_btn_text_surface = confirm_btn_font.render("Salvar", True, (255, 255, 255))
        confirm_btn_text_rect = confirm_btn_text_surface.get_rect(center = (pos_x, pos_y))

        confirm_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/frst_attack_button/default.png', 0.7)
        confirm_btn_rect = confirm_btn_graphic.get_rect(center = (pos_x - confirm_btn_text_surface.get_width() - 10, pos_y))

        quit_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/scd_attack_button/default.png', 0.7)
        quit_btn_rect = quit_btn_graphic.get_rect(midleft = (pos_x + 40, pos_y))

        quit_btn_font = pygame.font.Font(size=24)
        quit_btn_text_surface = quit_btn_font.render("Voltar", True, (255, 255, 255))
        quit_btn_text_rect = quit_btn_text_surface.get_rect(midleft = (pos_x + quit_btn_graphic.get_width() + 50, pos_y))

        self.display_surface.blit(select_btn_text_surface, select_btn_text_rect)

        self.display_surface.blit(confirm_btn_graphic, confirm_btn_rect)
        self.display_surface.blit(confirm_btn_text_surface, confirm_btn_text_rect)

        self.display_surface.blit(quit_btn_graphic, quit_btn_rect)
        self.display_surface.blit(quit_btn_text_surface, quit_btn_text_rect)

    def display_saved_text(self):
        if self.saved_time != 0 and self.saved_time >= pygame.time.get_ticks():
            saved_font = pygame.font.Font(size=24)
            saved_text_surface = saved_font.render("Configurações Salvas com Sucesso", True, (255, 255, 255))

            pos_x = self.display_surface.get_width() - 10
            pos_y = self.display_surface.get_height() - 64

            saved_text_rect = saved_text_surface.get_rect(midright = (pos_x, pos_y))

            self.display_surface.blit(saved_text_surface, saved_text_rect)
        else:
            self.saved_time = 0

    def format_values(self, value):
        if type(value) == bool:    
            if value == True:
                return "Sim"
            elif value == False:
                return "Não"
        elif type(value) == int:
            if value == 1:
                return "Fácil"
            elif value == 2:
                return "Médio"
            elif value == 3:
                return "Difícil"
        elif type(value) == list:
            return f"{value[0]}x{value[1]}"
        else:
            return str(value)

    def can_change_option(self, direction):
        options = list(self.options.keys())
        
        index = options.index(self.selected_option)

        if direction == 'up':
            return index - 1 >= 0
        elif direction == 'down':
            return index + 1 < len(options)
        
        return False

    def next_option(self):
        options = list(self.options.keys())
        
        index = options.index(self.selected_option)

        index += 1

        self.selected_option = options[index]

    def prev_option(self):
        options = list(self.options.keys())
        
        index = options.index(self.selected_option)

        index -= 1

        self.selected_option = options[index]

    def check_inputs(self):
        inputs = self.inputs.get_input()
        now = pygame.time.get_ticks()

        if inputs.is_unpausing() and now > self.button_clicked_time:
            self.pre_screen.is_config_screen = False
            
            self.button_clicked_time = now + 300
        elif inputs.is_walk_up() and self.can_change_option('up') and now > self.button_clicked_time:
            self.prev_option()
            
            self.button_clicked_time = now + 300
        elif inputs.is_walk_down() and self.can_change_option('down') and now > self.button_clicked_time:
            self.next_option()
            
            self.button_clicked_time = now + 300
        elif inputs.is_walk_right() and now > self.button_clicked_time:
            options = self.settings_options[self.selected_option]
            value_index = options.index(self.settings[self.selected_option])

            if value_index + 1 < len(options):
                self.settings[self.selected_option] = options[value_index + 1]
            
            self.button_clicked_time = now + 300
        elif inputs.is_walk_left() and now > self.button_clicked_time:
            options = self.settings_options[self.selected_option]
            value_index = options.index(self.settings[self.selected_option])

            if value_index - 1 >= 0:
                self.settings[self.selected_option] = options[value_index - 1]
            
            self.button_clicked_time = now + 300
        elif inputs.is_selecting() and now > self.button_clicked_time:
            for key, value in self.settings.items():
                change_settings_value(key, value)

                self.saved_time = pygame.time.get_ticks() + 3000

            self.button_clicked_time = now + 300