import pygame
from utils.enums import OpenMapTileType
from settings import TILESIZE, ZOOM

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, original_pos: tuple, groups: list, sprite_type: str, surface = pygame.Surface((TILESIZE * ZOOM, TILESIZE * ZOOM))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface
        self.original_pos = original_pos

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -5)