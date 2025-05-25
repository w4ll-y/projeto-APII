import pygame
from settings import WORLD_MAP, TILESIZE
from utils.enums import LevelType, OpenMapTileType
from levels.tile import Tile
from entities.player import Player

class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.level_map(LevelType.OPENMAP)

    def create_map(self, level_map):
        for row_index, row in enumerate(level_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], OpenMapTileType.ROCK)
                if col == 'p':
                    Player((x, y), [self.visible_sprites], self.obstacles_sprites)

    def level_map(self, level_type):
        match level_type:
            case LevelType.OPENMAP:
                self.create_map(WORLD_MAP)
            case LevelType.DUNGEON:
                self.create_map(WORLD_MAP)

    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
        