import pygame
from settings import WORLD_MAP, TILESIZE
from utils.enums import LevelType, OpenMapTileType, BoundaryTyleTipe
from utils.suport import import_csv_layout, import_folder
from levels.tile import Tile
from entities.player import Player

class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.level_map(LevelType.OPENMAP)

    def create_map(self, level_map: list):
        layouts = {
            #style: layout
            'boundary': import_csv_layout('./assets/map/map_Boundary.csv'),
            'objects': import_csv_layout('./assets/map/map_Objects.csv'),
            'monuments': import_csv_layout('./assets/map/map_Monuments.csv')
        }

        graphics = {
            'objects': import_folder('./assets/graphics/objects'),
            'monuments': import_folder('./assets/graphics/monuments')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE    

                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'objects':
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surface)
                        if style == 'monuments':
                            surface = graphics['monuments'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'monuments', surface)
        
        self.player = Player((600, 600), [self.visible_sprites], self.obstacles_sprites)

    def level_map(self, level_type: str):
        match level_type:
            case LevelType.OPENMAP:
                self.create_map(WORLD_MAP)
            case LevelType.DUNGEON:
                self.create_map(WORLD_MAP)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.save_window_size()

        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('./assets/graphics/tilesmap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def save_window_size(self):
        self.display_surface = pygame.display.get_surface()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player: Player):

        #player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth

        #floor offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        