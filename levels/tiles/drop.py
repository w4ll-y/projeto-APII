import pygame
from utils.enums import DropType
from utils.suport import *
from entities.player import Player
from settings import DEFAULT_ACTUAL_STATS_VALUE

class Drop(pygame.sprite.Sprite):
    def __init__(self, groups, drop_type: DropType, pos: dict):
        super().__init__(groups)

        self.sprite_type = 'drop'
        self.drop_type = drop_type
        self.image: pygame.Surface = self.get_image()

        self.pos = pos

        self.rect = self.image.get_rect(**self.pos)
        self.hitbox = self.rect.inflate(self.image.get_width() - 10, self.image.get_height() - 10)

    def get_image(self):
        base_path = 'assets/graphics/collectibles/drops/'

        match self.drop_type:
            case DropType.HEALTH:
                return resize_image(base_path + '00.png', 0.6)
            case DropType.BULLET:
                return resize_image(base_path + '01.png', 1.4)
    
    def interaction(self, player: Player):
        if player.hitbox.colliderect(self.hitbox):
            match self.drop_type:
                case DropType.HEALTH:
                    if player.stats['health'] > player.actual_stats['health']:
                        player.actual_stats['health'] += DEFAULT_ACTUAL_STATS_VALUE
                case DropType.BULLET:
                    if player.stats['bullets'] > player.actual_stats['bullets']:
                        player.actual_stats['bullets'] += 1
                    
            self.kill()
