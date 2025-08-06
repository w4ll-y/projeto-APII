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
            return 'assets/sprites/hud/health/full_health.png'
        elif health - player_health == DEFAULT_ACTUAL_HEALTH_VALUE:
            return 'assets/sprites/hud/health/mid_health.png'
        else:
            return 'assets/sprites/hud/health/empty_health.png'

    def show_health(self, player_health, player_max_health):
        for index, health in enumerate(range(DEFAULT_HEALTH_VALUE, player_max_health + 1, DEFAULT_HEALTH_VALUE)):
            heart = resize_image(self.health_state_path(index, health, player_health), 1.7)
            heart_rect = heart.get_rect()

            heart_rect.topleft = (index * HEALTH_WIDTH + 10, 10)
            heart_rect.width = HEALTH_WIDTH
            heart_rect.height = HEALTH_HEIGHT

            self.display_surface.blit(heart, heart_rect)

    def show_frt_hand_weapons(self, weapon_index: int):
        bg_rect = pygame.Rect(50, self.display_surface.get_height() - 200, ITEM_BOX_SIZE, ITEM_BOX_SIZE)

        weapon_name = list(WEAPON_DATA.keys())[weapon_index]
        weapon_graphic = resize_image(WEAPON_DATA[weapon_name]["graphic"], 1.5)
        weapon_rect = weapon_graphic.get_rect(center= bg_rect.center)

        pygame.draw.rect(self.display_surface, UI_BOX_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BOX_BORDER_COLOR, bg_rect, 3)
        self.display_surface.blit(weapon_graphic, weapon_rect)
    
    def show_scd_hand_weapons(self):
        bg_rect = pygame.Rect(60 + ITEM_BOX_SIZE, self.display_surface.get_height() - 180, ITEM_BOX_SIZE - 20, ITEM_BOX_SIZE - 20)

        pygame.draw.rect(self.display_surface, UI_BOX_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BOX_BORDER_COLOR, bg_rect, 3)

    def display(self, player: Player):
        self.show_health(player.actual_stats["health"], player.stats["health"])
        self.show_frt_hand_weapons(player.weapon_index)
        self.show_scd_hand_weapons()