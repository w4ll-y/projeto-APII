import pygame
from utils.enums import DropType
from utils.suport import *
from entities.player import Player
from settings import DEFAULT_ACTUAL_STATS_VALUE, DEFAULT_ENERGY_STATS_VALUE

class Drop(pygame.sprite.Sprite):
    def __init__(self, groups, drop_type: DropType, pos: dict):
        super().__init__(groups)

        self.sprite_type = 'drop'
        self.drop_type = drop_type
        self.image: pygame.Surface = self.get_image()

        self.pos = pos

        self.rect = self.image.get_rect(**self.pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def get_image(self):
        base_path = 'assets/graphics/collectibles/drops/'

        match self.drop_type:
            case DropType.HEALTH:
                return resize_image(base_path + '0.png', 0.8)
            case DropType.ENERGY:
                return resize_image(base_path + '1.png', 0.8)
    
    def interaction(self, player: Player):
        if player.hitbox.colliderect(self.hitbox):
            match self.drop_type:
                case DropType.HEALTH:
                    if player.stats['health'] > player.actual_stats['health']:
                        player.actual_stats['health'] += DEFAULT_ACTUAL_STATS_VALUE
                case DropType.ENERGY:
                    if player.stats['energy'] > player.actual_stats['energy']:
                        player.actual_stats['energy'] += DEFAULT_ENERGY_STATS_VALUE * 2
                    
            self.kill()
