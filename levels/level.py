import pygame
from settings import WORLD_MAP, TILESIZE, ZOOM
from utils.enums import LevelType
from utils.suport import import_csv_layout, import_folder, resize_image, change_value_in_csv
from levels.tile import Tile
from entities.player import Player

class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.level_map(LevelType.OPENMAP)

    def create_map(self, level_map: list):
        self.layouts = {
            #style: layout
            'boundary': import_csv_layout('./storage/map/map_Boundary.csv'),
            'objects': import_csv_layout('./storage/map/map_Objects.csv'),
            'monuments': import_csv_layout('./storage/map/map_Monuments.csv'),
            'interactives': import_csv_layout('./storage/map/map_Interactives.csv'),
        }

        self.graphics = {
            'objects': import_folder('./assets/graphics/objects'),
            'monuments': import_folder('./assets/graphics/monuments'),
            'interactives': import_folder('./assets/graphics/interactives')
        }

        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE * ZOOM
                        y = row_index * TILESIZE * ZOOM

                        if style == 'boundary':
                            Tile((x, y), (row_index, col_index), int(col), [self.obstacles_sprites], 'invisible')
                        if style == 'objects':
                            surface = self.graphics['objects'][int(col)]

                            Tile((x, y), (row_index, col_index), int(col), [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], 'object', surface)
                        if style == 'monuments':
                            surface = self.graphics['monuments'][int(col)]
                            
                            Tile((x, y), (row_index, col_index), int(col), [self.visible_sprites, self.obstacles_sprites], 'monuments', surface)
                        if style == 'interactives':
                            surface = self.graphics['interactives'][int(col)]

                            Tile((x, y), (row_index, col_index), int(col), [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], 'interactive', surface)
        
        self.player = Player((1200, 1200), [self.visible_sprites, self.attack_sprites], self.obstacles_sprites)

    def level_map(self, level_type: str):
        match level_type:
            case LevelType.OPENMAP:
                self.create_map(WORLD_MAP)
            case LevelType.DUNGEON:
                self.create_map(WORLD_MAP)

    def player_attack_logic(self, player: Player):
        if player.attacking:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)

                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'object':
                            target_sprite.kill()
                            change_value_in_csv('./storage/map/map_Objects.csv', target_sprite.original_pos, -1) #-1 = empty space in map
                        if target_sprite.sprite_type == 'interactive':
                            target_sprite.image = self.graphics['interactives'][target_sprite.original_value + 1] 
                            change_value_in_csv('./storage/map/map_Interactives.csv', target_sprite.original_pos, target_sprite.original_value + 1) #get the next tile Sprite

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.player_attack_logic(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.save_window_size()

        self.offset = pygame.math.Vector2()

        self.floor_surface = resize_image('./assets/graphics/tilesmap/ground.png')

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
        