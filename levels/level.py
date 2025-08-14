import pygame
import time
from random import shuffle
from settings import TILESIZE, ZOOM
from utils.enums import LevelType
from utils.suport import *
from levels.tile import Tile
from levels.tiles.interactives import Interactives
from entities.player import Player
from entities.weapons import Weapon
from ui.hud import Hud
from inputs.input_manager import InputManager
from entities.enemy import Enemy
from ui.menu.pause import Pause
from ui.menu.main_menu import MainMenu
from ui.history import History

class Level:
    def __init__(self, level_map: LevelType, finish_game_time = [time.time() + 600]):
        pygame.mixer.quit()
        pygame.mixer.init()

        if [LevelType.MAINMENU, LevelType.HISTORY].count(level_map) == 0:
            #O tempo para finalizar o jogo é salvo em uma lista porque, quando uma lista é passada
            #como parâmetro, eu posso alterar o valor original em outra parte do código.
            #Uma variável comum, quando passada como parâmetro, altera uma cópia criada para aquela parte do código, o valor original nâo é alterado
            self.finish_game_time = finish_game_time
            self.hud = Hud(self.inputs, self.finish_game_time)
            self.pause = Pause(self.inputs, self, self.finish_game_time)

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.player_sprite = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_attack = None

        self.inputs = InputManager()

        self.music_folder = 'assets/musics/background'        
        self.music_channel = pygame.mixer.find_channel()
        self.music_channel.set_volume(0.4)
        self.music_channel.fadeout(800)

        self.player = None

        self.main_menu = MainMenu(self.inputs, self)
        self.is_main_menu = False

        self.history = History(self.inputs, self)
        self.is_history = False

        self.created_map = time.time()
        self.level_map(level_map)

    def reset(self, level_map, finish_game_time):
        self.__init__(level_map, finish_game_time)

    def set_musics(self):
        musics = import_folder_files(self.music_folder)
        shuffle(musics)

        sound = pygame.mixer.Sound(musics[0])
        self.music_channel.play(sound)
        
        for i in range(1, len(musics)):
            sound = pygame.mixer.Sound(musics[i])
            self.music_channel.queue(sound)

    def set_input_type(self, events):
        self.inputs.set_input_type(events)

    def create_map(self):
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
            'objects': import_folder_resize_image('./assets/graphics/objects'),
            'interactives': import_folder_resize_image('./assets/graphics/interactives')
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
                                self.player = Player((x, y), [self.visible_sprites, self.player_sprite], self.obstacles_sprites, self.create_attack, self.destroy_attack, self.inputs, self.pause)
                            else:
                                Enemy(int(col), (x,y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player, [self.visible_sprites, self.interaction_sprites])

        self.finish_game_time[0] += time.time() - self.created_map
        self.created_map = 0

    def play_music(self):        
        if self.player is not None:
            if self.player.paused_game:
                self.music_channel.pause()
            else:
                self.music_channel.unpause()
            
        if not self.music_channel.get_busy():
            self.set_musics()

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self,amount, attack_type):
            if self.player.vulnerable:
                if self.player.actual_stats['health'] - amount >= 0:
                    self.player.actual_stats['health'] -= amount
                else:
                    self.player.actual_stats['health'] = 0
                self.player.vulnerable = False
                self.player.hurt_time = pygame.time.get_ticks()

    def level_map(self, level_type: str):
        match level_type:
            case LevelType.OPENMAP:
                self.music_folder = 'assets/musics/background'

                self.create_map()
            case LevelType.MAINMENU:
                self.music_folder = 'assets/musics/menu'

                self.is_main_menu = True
            case LevelType.HISTORY:
                self.music_folder = ''

                self.is_history = True

    def player_attack_collision(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                colision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if colision_sprites:
                    for target_sprite in colision_sprites:
                        if target_sprite.sprite_type == 'interactive':
                            if target_sprite.destructive == True:
                                target_sprite.drop([self.visible_sprites, self.interaction_sprites])
                                target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damaged(self.player,attack_sprite.sprite_type)

    def interaction_collision(self, player: Player):
        collision_sprites = pygame.sprite.spritecollide(self.player_sprite.sprites()[0], self.interaction_sprites, False)

        if collision_sprites:
            for target_sprite in collision_sprites:
                if target_sprite.sprite_type == 'interactive':
                    target_sprite.special_function(player, self.visible_sprites.offset.x, self.visible_sprites.offset.y, self.inputs, self.graphics['interactives'], self.layouts['interactives_chest_items'])
                elif target_sprite.sprite_type == 'drop':
                    target_sprite.interaction(self.player)

    def run(self, events):
        if self.is_history:
            self.history.display_text()
            return

        self.play_music()

        if self.is_main_menu:
            self.main_menu.display_menu()
            return
        
        if self.created_map != 0:
            return
        
        self.set_input_type(events)
        self.visible_sprites.custom_draw(self.player)
        self.interaction_collision(self.player)
        self.player_attack_collision()
        self.visible_sprites.enemy_update(self.player)
        self.hud.display(self.player)
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
        
    def enemy_update(self,player):
        enemy_sprite = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprite:
            enemy.enemy_update(player)