import pygame
from utils.enums import OpenMapTileType

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type):
        super().__init__(groups)

        self.tile_type = tile_type

        self.set_image()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

    def set_image(self):
        match self.tile_type:
            case OpenMapTileType.ROCK:
                self.image = pygame.image.load('assets/images/openmap/rock.png').convert_alpha()