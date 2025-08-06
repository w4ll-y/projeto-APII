import pygame
from entities.player import Player
from settings import * 
from utils.suport import resize_image

class Hud:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
    
    def health_state_path(self, index: int, health: int, player_health: int):
        compare_health = player_health - health

        if health <= player_health:
            return 'assets/graphics/hud/health/full_health.png'
        elif health - player_health == DEFAULT_ACTUAL_STATS_VALUE:
            return 'assets/graphics/hud/health/mid_health.png'
        else:
            return 'assets/graphics/hud/health/empty_health.png'
    
    def button_graphic(self, player_action: bool, button_name: str):
        if player_action:
            return f'assets/graphics/hud/keyboard/{button_name}/pressed.png'
        
        return f'assets/graphics/hud/keyboard/{button_name}/default.png'

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

        key_graphic = resize_image(self.button_graphic(player_attacking, 'n_button'), 0.8)
        key_rect = key_graphic.get_rect(center= (bg_rect.left + 5, bg_rect.bottom - 5))

        change_weapon_key_graphic = resize_image(self.button_graphic(change_weapon, 'q_button'), 0.6)
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

        key_graphic = resize_image(self.button_graphic(player_action, 'm_button'), 0.7)
        key_rect = key_graphic.get_rect(center= (bg_rect.left + 5, bg_rect.bottom - 5))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        self.display_surface.blit(key_graphic, key_rect)

    def display(self, player: Player):
        self.show_health(player.actual_stats["health"], player.stats["health"])
        self.show_energy_bar(player.actual_stats["energy"], player.stats["energy"])
        self.show_frt_hand_weapons(player.actual_stats["energy"], player.weapon, player.attacking, not player.can_switch_weapon)
        self.show_scd_hand_weapons(player.scd_attacking)