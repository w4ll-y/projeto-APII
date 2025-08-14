import pygame
import time
from entities.player import Player
from settings import * 
from utils.suport import resize_image, import_folder_resize_image
from inputs.input_manager import InputManager
from utils.enums import InputType

class Hud:
    def __init__(self, inputs: InputManager, finish_game_time: float):
        self.inputs = inputs
        self.display_surface = pygame.display.get_surface()

        self.clock_sprites = import_folder_resize_image('assets/sprites/hud/clock', 0.7)
        self.actual_clock_sprite = 0
        self.time_to_change_sprite = pygame.time.get_ticks() + 800

        self.paused_game = False
        self.paused_time = 0
        self.paused_start = 0

        self.finish_game_time = finish_game_time
    
    def health_state_path(self, index: int, health: int, player_health: int):
        if health <= player_health:
            return 'assets/graphics/hud/health/full_health.png'
        elif health - player_health == DEFAULT_ACTUAL_STATS_VALUE:
            return 'assets/graphics/hud/health/mid_health.png'
        else:
            return 'assets/graphics/hud/health/empty_health.png'
    
    def button_graphic(self, player_action: bool, button_name: str):
        selected_input = self.inputs.get_input()
        
        return f'assets/graphics/hud/inputs/{'keyboard' if selected_input.type == InputType.KEYBOARD else 'joystick'}/{button_name}/{'default' if not player_action else 'pressed'}.png'

    def show_health(self, player_health, player_max_health):
        for index, health in enumerate(range(DEFAULT_STATS_VALUE, player_max_health + 1, DEFAULT_STATS_VALUE)):
            heart_graphic = resize_image(self.health_state_path(index, health, player_health), 1.7)
            heart_rect = heart_graphic.get_rect()

            heart_rect.topleft = (index * HEALTH_WIDTH + 10, 10)
            heart_rect.width = HEALTH_WIDTH
            heart_rect.height = HEALTH_HEIGHT

            self.display_surface.blit(heart_graphic, heart_rect)

    def show_energy_bar(self, player_energy, player_max_energy):
        energy_bar = pygame.Rect(20, HEALTH_HEIGHT, player_energy  * 3, BAR_HEIGHT)
        max_energy_bar = pygame.Rect(20, HEALTH_HEIGHT, player_max_energy * 3, BAR_HEIGHT)

        energy_graphic = resize_image('assets/graphics/hud/energy/energy.png', 0.06)
        energy_rect = energy_graphic.get_rect(center= (energy_bar.left, energy_bar.centery))

        pygame.draw.rect(self.display_surface, ENERGY_COLOR, energy_bar)
        pygame.draw.rect(self.display_surface, ENERGY_BORDER_COLOR, max_energy_bar, 3)
        self.display_surface.blit(energy_graphic, energy_rect)

    def show_frt_hand_weapons(self, player_energy: int, player_weapon: dict, player_attacking: bool, change_weapon: bool):
        bg_rect = pygame.Rect(50, self.display_surface.get_height() - 200, ITEM_BOX_SIZE, ITEM_BOX_SIZE)

        weapon_graphic = resize_image(player_weapon["graphic"], 1.5)
        weapon_rect = weapon_graphic.get_rect(center= bg_rect.center)

        key_graphic = resize_image(self.button_graphic(player_attacking, 'frst_attack_button'), 0.8)
        key_rect = key_graphic.get_rect(center= (bg_rect.left + 5, bg_rect.bottom - 5))

        change_weapon_key_graphic = resize_image(self.button_graphic(change_weapon, 'change_weapon'), 0.6)
        change_weapon_key_rect = change_weapon_key_graphic.get_rect(center= (bg_rect.left + 20, bg_rect.top + 20))

        change_weapon_graphic = resize_image('assets/graphics/hud/weapon/change_weapon.png', 0.12)
        change_weapon_rect = change_weapon_graphic.get_rect(center= (bg_rect.left + change_weapon_key_rect.width + 15, bg_rect.top + 20))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR if player_energy >= player_weapon["energy_spent"] else 'red', bg_rect, 3)
        self.display_surface.blit(weapon_graphic, weapon_rect)
        self.display_surface.blit(key_graphic, key_rect)
        self.display_surface.blit(change_weapon_key_graphic, change_weapon_key_rect)
        self.display_surface.blit(change_weapon_graphic, change_weapon_rect)
    
    def show_scd_hand_weapons(self, player_action: bool):
        bg_rect = pygame.Rect(70 + ITEM_BOX_SIZE, self.display_surface.get_height() - 180, ITEM_BOX_SIZE - 20, ITEM_BOX_SIZE - 20)

        key_graphic = resize_image(self.button_graphic(player_action, 'scd_attack_button'), 0.7)
        key_rect = key_graphic.get_rect(center= (bg_rect.left + 5, bg_rect.bottom - 5))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        self.display_surface.blit(key_graphic, key_rect)
    
    def show_getted_item(self, player: Player):
        if player.getting_item is not None:
            image = player.getting_item['item_graphic']
            rect = player.getting_item['item_rect']

            self.display_surface.blit(image, rect)

    def show_time_to_finish(self):
        if pygame.time.get_ticks() >= self.time_to_change_sprite and not self.paused_game:
            self.actual_clock_sprite = self.actual_clock_sprite + 1 if self.actual_clock_sprite < len(self.clock_sprites) - 1 else 0

            self.time_to_change_sprite = pygame.time.get_ticks() + 800

        time_to_finish = self.finish_game_time[0] - time.time()

        if self.paused_game:
            time_to_finish = self.paused_time

        minutes = int((time_to_finish // 60) % 60)
        seconds = int(time_to_finish % 60)
        milisec = int((time_to_finish % 1) * 1000)

        time_text = f'{minutes:02d}:{seconds:02d}:{milisec:03d}'

        font = pygame.font.Font(size=36)
        text_surface = font.render(time_text, True, (255, 255, 255) if time_to_finish > 60 else (255,  80, 0))

        pos_x = self.display_surface.get_width() - text_surface.get_width() - 30
        pos_y = 30

        text_rect = text_surface.get_rect(center = (pos_x, pos_y))

        #clock sprite
        clock_surface = self.clock_sprites[self.actual_clock_sprite]
        clock_rect = clock_surface.get_rect(center= (pos_x - 80, pos_y))

        self.display_surface.blit(clock_surface, clock_rect)
        self.display_surface.blit(text_surface, text_rect)

    def display(self, player: Player):
        if player.paused_game and not self.paused_game:
            self.paused_game = True
            self.paused_start = time.time()
            self.paused_time = self.finish_game_time[0] - self.paused_start
        elif not player.paused_game:
            self.paused_game = False

            if self.paused_start != 0:
                self.finish_game_time[0] += time.time() - self.paused_start
                self.paused_start = 0

        self.show_health(player.actual_stats["health"], player.stats["health"])
        self.show_energy_bar(player.actual_stats["energy"], player.stats["energy"])
        self.show_frt_hand_weapons(player.actual_stats["energy"], player.weapon, player.attacking, not player.can_switch_weapon)
        self.show_scd_hand_weapons(player.scd_attacking)
        self.show_getted_item(player)
        self.show_time_to_finish()