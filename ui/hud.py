import pygame
from entities.player import Player
from settings import * 
from utils.suport import resize_image

class Hud:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

    def show_health(self, player_health, player_max_health):
        for index, health in enumerate(range(0, player_max_health, 25)):
            heart = pygame.image.load('assets/sprites/hud/health/full_health.png')
            heart_rect = heart.get_rect()

            heart_rect.topleft = (index * HEALTH_WIDTH + 10, 10)
            heart_rect.width = HEALTH_WIDTH
            heart_rect.height = HEALTH_HEIGHT

            pygame.draw.rect(self.display_surface, 'black', heart_rect)

    def display(self, player: Player):
        self.show_health(player.actual_stats["health"], player.stats["health"])