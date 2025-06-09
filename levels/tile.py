import pygame
from utils.enums import OpenMapTileType
from settings import TILESIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list, sprite_type: str, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface

        if self.sprite_type == 'invisible':
            self.image.set_alpha(0)

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)