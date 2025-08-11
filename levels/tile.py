import pygame
from utils.enums import OpenMapTileType
from settings import TILESIZE, ZOOM

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: dict, original_pos: tuple, original_value: int, groups: list, sprite_type: str, surface = pygame.Surface((TILESIZE * ZOOM, TILESIZE * ZOOM)), activated: bool | None = None, inflate_ajust: tuple = (0, -5), hitbox_ajust: tuple = (0,0, 0, 0)):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface
        
        self.original_pos = original_pos
        self.original_value = original_value

        self.activated = activated

        self.rect = self.image.get_rect(**pos)
        self.hitbox = self.rect.inflate(*inflate_ajust)

        self.hitbox.width -= hitbox_ajust[0]
        self.hitbox.height += hitbox_ajust[1]

        self.hitbox.left -= hitbox_ajust[2]
        self.hitbox.top -= hitbox_ajust[3]