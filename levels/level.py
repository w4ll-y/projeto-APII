import pygame
from settings import WORLD_MAP, TILESIZE, ZOOM
from utils.enums import LevelType
from utils.suport import *
from levels.tile import Tile
from levels.tiles.interactives import Interactives
from entities.player import Player
from entities.weapons import Weapon
from ui.hud import Hud
from inputs.input_manager import InputManager
from entities.enemy import Enemy

class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_attack = None

        self.inputs = InputManager()
        self.hud = Hud(self.inputs)

        self.level_map(LevelType.OPENMAP)

    def set_input_type(self, events):
        self.inputs.set_input_type(events)

    def create_map(self, level_map: list):
        self.layouts = {
            #style: layout
            'boundary': import_csv_layout('./storage/map/map_Boundary.csv'),
            'objects': import_csv_layout('./storage/map/map_Objects.csv'),
            'interactives': import_csv_layout('./storage/map/map_Interactives.csv'),
            'interactives_activated': import_csv_layout('./storage/map/map_Interactives_Activated.csv'),
            'interactives_chest_items': import_csv_layout('./storage/map/map_Interactives_Chest_Items.csv'),
            'entities': import_csv_layout('./storage/map/map_Entities.csv')
        }

        self.graphics = {
            'objects': import_folder('./assets/graphics/objects'),
            'interactives': import_folder('./assets/graphics/interactives')
        }

        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE * ZOOM
                        y = row_index * TILESIZE * ZOOM
                        col_value = int(col)

                        if style == 'boundary':
                            Tile({'topleft': (x,y)}, (row_index, col_index), col_value, [self.obstacles_sprites], 'invisible')
                        if style == 'objects':
                            surface = self.graphics['objects'][col_value]

                            Tile({'midleft': (x,y)}, (row_index, col_index), col_value, [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], 'object', surface, inflate_ajust=obj_inflate_ajust(col_value), hitbox_ajust=obj_hitbox_ajust(col_value))
                        if style == 'interactives':
                            surface = self.graphics['interactives'][col_value]
                            activated = self.layouts['interactives_activated'][row_index][col_index]
                            destructive = is_icv_destructive(col_value)
                            next_value = icv_next_value(col_value)

                            Interactives({'topleft': (x,y)}, (row_index, col_index), col_value, [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites, self.interaction_sprites], 'interactive', surface, activated, destructive=destructive, next_value=next_value)
        
                        if style == 'entities':
                            if col == '1':
                                self.player = Player((x, y), [self.visible_sprites, self.attack_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack, self.inputs)
                            else:
                                Enemy(col_value, (x,y), [self.visible_sprites], self.obstacles_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

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
                        if target_sprite.sprite_type == 'interactive':
                            if target_sprite.destructive == True:
                                target_sprite.drop([self.visible_sprites, self.interaction_sprites])
                                target_sprite.kill()

    def interaction_logic(self, player: Player):
        for attack_sprite in self.attack_sprites:
            collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.interaction_sprites, False)

            if collision_sprites:
                for target_sprite in collision_sprites:
                    if target_sprite.sprite_type == 'interactive':
                        target_sprite.special_function(player, self.visible_sprites.offset.x, self.visible_sprites.offset.y, self.inputs, self.graphics['interactives'], self.layouts['interactives_chest_items'])
                    elif target_sprite.sprite_type == 'drop':
                        target_sprite.interaction(self.player)

    def run(self, events):
        self.set_input_type(events)
        self.visible_sprites.custom_draw(self.player)
        self.player_attack_logic(self.player)
        self.interaction_logic(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.hud.display(self.player)

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
        
    def enemy_update(self,player):
        enemy_sprite = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprite:
            enemy.enemy_update(player)