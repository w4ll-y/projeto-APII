import pygame
import time
from inputs.input_manager import InputManager
from utils.suport import reset_game, resize_image, new_endgame_time
from utils.enums import LevelType, InputType

class EndGameMenu:
    def __init__(self, inputs: InputManager, level):
        self.inputs = inputs
        self.level = level
        self.finish_game_time = None

        self.display_surface = pygame.display.get_surface()

        self.options = ["Reiniciar", "Sair para o Menu"]
        self.selected_option = 0

        self.button_clicked_time = pygame.time.get_ticks()

        self.created_at = None
        self.start_time = None

    def set_finish_game_time(self, time_to_end):
        time_to_finish = time_to_end - time.time()

        minutes = int((time_to_finish // 60) % 60)
        seconds = int(time_to_finish % 60)
        milisec = int((time_to_finish % 1) * 1000)

        time_text = f'{minutes:02d}:{seconds:02d}:{milisec:03d}'

        self.finish_game_time = time_text

        new_endgame_time(time_text)

    def display_menu(self): 
        if not self.created_at:
            self.start_time = pygame.time.get_ticks()
            self.created_at = self.start_time + 1000

        now = pygame.time.get_ticks()
        progress = (now - self.start_time) / (self.created_at - self.start_time)
        progress = max(0, min(1, progress))

        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(progress * 255))

        self.display_surface.blit(overlay, (0, 0))

        pos_x = self.display_surface.get_width() // 2
        pos_y = self.display_surface.get_height() // 2

        player_graphic = resize_image(f'assets/sprites/player/down/protafrente1.png', 1)
        player_rect = player_graphic.get_rect(center= (pos_x, pos_y))

        pc_graphic = resize_image(f'assets/sprites/special_entity/PadreCicero1.png', 1)
        pc_graphic.set_alpha(int(progress * 255))
        pc_rect = pc_graphic.get_rect(center= (pos_x + player_graphic.get_width() + 15, pos_y))

        font = pygame.font.Font(size=36)
        gameover_surface = font.render("Parabéns, você completou o jogo com:", True, (255, 0, 0))
        gameover_rect = gameover_surface.get_rect(center = (pos_x, pos_y - player_graphic.get_height() - 100))

        font = pygame.font.Font(size=36)
        time_surface = font.render(self.finish_game_time, True, (255, 255, 255))
        time_rect = time_surface.get_rect(center = (pos_x, pos_y - player_graphic.get_height() - 60))

        #display buttons
        select_btn_font = pygame.font.Font(size=24)
        select_btn_text_surface = select_btn_font.render("Selecionar", True, (255, 255, 255))
        select_btn_text_rect = select_btn_text_surface.get_rect(center = (pos_x, pos_y * 2 - 60))

        select_btn_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if self.inputs.get_input().type == InputType.KEYBOARD else 'joystick'}/frst_attack_button/default.png', 1)
        select_btn_rect = select_btn_graphic.get_rect(center= (pos_x - select_btn_text_surface.get_width(), pos_y * 2 - 60))

        self.display_surface.blit(gameover_surface, gameover_rect)
        self.display_surface.blit(time_surface, time_rect)
        self.display_surface.blit(player_graphic, player_rect)
        self.display_surface.blit(pc_graphic, pc_rect)
        self.display_surface.blit(select_btn_graphic, select_btn_rect)
        self.display_surface.blit(select_btn_text_surface, select_btn_text_rect)

        for index, text in enumerate(self.options):
            font = pygame.font.Font(size=36)
            text_surface = font.render(text, True, (128, 128, 128) if index != self.selected_option else (255, 255, 255))

            pos_x = self.display_surface.get_width() // 2
            pos_y = self.display_surface.get_height() // 2 + (64 * index)

            text_rect = text_surface.get_rect(center = (pos_x, pos_y + player_graphic.get_height()))

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
                    reset_game()
                    self.level.reset(LevelType.MAINMENU, self.level.settings, [time.time() + 600])

            self.button_clicked_time = now + 300