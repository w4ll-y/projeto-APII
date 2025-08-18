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
from ui.menu.game_over import GameOver
from ui.history import History
from core.config import Config
from entities.guns import GunsPlayer
from entities.bullets import Bullet

class Level:
    def __init__(self, level_map: LevelType, settings: Config, player_position: tuple | None = (53, 83), finish_game_time = [time.time() + 600], player_stats: dict = read_json('data/player_info.json'), player_actual_stats: dict = read_json('data/player_info.json'), player_numb_weapons: list = [0], player_numb_guns: list = [1]):
        self.settings = settings
        pygame.mixer.quit()
        pygame.mixer.init()

        self.level_map_type = level_map
        self.map_path = ''

        self.player_stats = player_stats
        self.player_actual_stats = player_actual_stats
        self.player_numb_weapons = player_numb_weapons
        self.player_numb_guns = player_numb_guns

        if [LevelType.MAINMENU, LevelType.HISTORY].count(self.level_map_type) == 0:
            #O tempo para finalizar o jogo é salvo em uma lista porque, quando uma lista é passada
            #como parâmetro, eu posso alterar o valor original em outra parte do código.
            #Uma variável comum, quando passada como parâmetro, altera uma cópia criada para aquela parte do código, o valor original nâo é alterado
            self.finish_game_time = finish_game_time
            self.finish_game_time[0] += 1.2
            self.hud = Hud(self.inputs, self.finish_game_time)
            self.pause = Pause(self.inputs, self, self.finish_game_time)
            self.map_path = f'./assets/graphics/tilesmap/{level_map.value}/ground.png'

        self.player_position = player_position
        
        self.visible_sprites = YSortCameraGroup(self.map_path)
        self.obstacles_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.player_sprite = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_attack = None

        self.inputs = InputManager()

        self.music_folder = 'assets/musics/background'  
        self.music_channel = pygame.mixer.find_channel()
        self.music_channel.fadeout(800)

        self.player = None
        self.enemy = None

        self.main_menu = MainMenu(self.inputs, self)
        self.is_main_menu = False

        self.history = History(self.inputs, self)
        self.is_history = False

        self.gameover_menu = GameOver(self.inputs, self)
        self.is_gameover_menu = False

        self.created_map = time.time()
        self.level_map(level_map)

    def reset(self, level_map, settings, finish_game_time, player_position: tuple | None = None, player_stats: dict | None = None, player_actual_stats: dict | None = None, player_numb_weapons: list | None = None, player_numb_guns: list | None = None):
        if player_position is None: player_position = (53, 83)
        if player_stats is None: player_stats = read_json('data/player_info.json')
        if player_actual_stats is None: player_actual_stats = read_json('data/player_info.json')
        if player_numb_weapons is None: player_numb_weapons = [0]
        if player_numb_guns is None: player_numb_guns = [1]

        self.__init__(level_map, settings, player_position, finish_game_time, player_stats, player_actual_stats, player_numb_weapons, player_numb_guns)

    def special_function(self):
        if self.level_map_type == LevelType.DUNGEON:
            if len(self.player.numb_weapons) > 1:
                for sprite in self.interaction_sprites.sprites():
                    if sprite.sprite_type == 'enemy':
                        sprite.kill()
            if len(self.attackable_sprites) == 8 or len(self.player.numb_weapons) > 1:
                for sprite in self.interaction_sprites.sprites():
                    if sprite.sprite_type == 'interactive':
                        if sprite.original_value == 6:
                            change_value_in_csv('./storage/open_map/map_Interactives.csv', sprite.original_pos, sprite.next_value)
                            sprite.image = self.graphics['interactives'][sprite.next_value]
                            sprite.original_value = sprite.next_value
                        if sprite.original_value == 8:
                            sprite.kill()

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

    def create_map(self, layouts):
        self.layouts = {}

        for layout in layouts:
            self.layouts[layout] = import_csv_layout(f'./storage/{self.level_map_type.value}/{layout_file(layout)}')

        self.graphics = {
            'objects': import_folder_resize_image(f'./assets/graphics/objects'),
            'interactives': import_folder_resize_image(f'./assets/graphics/interactives')
        }

        for style, layout in self.layouts.items():
            if style == 'entities':
                layout[self.player_position[0]][self.player_position[1]] = '1'

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
                            activated = self.layouts['interactives_activated'][row_index][col_index] if 'interactives_activated' in list(self.layouts.keys()) else False
                            destructive = is_icv_destructive(col_value)
                            next_value = icv_next_value(col_value)

                            Interactives({'topleft': (x,y)}, (row_index, col_index), col_value, [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites, self.interaction_sprites], 'interactive', surface, activated, destructive=destructive, next_value=next_value)
        
                        if style == 'entities':
                            if col == '1':
                                self.player = Player((x, y), [self.visible_sprites, self.player_sprite], self.obstacles_sprites, self.create_attack, self.destroy_attack, self.inputs, self.pause, self.create_gun_attack, self, self.player_stats, self.player_actual_stats, self.player_numb_weapons, self.player_numb_guns)
                            else:
                                self.enemy = Enemy(int(col), (x,y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player, [self.visible_sprites, self.interaction_sprites], self.settings, self.create_gun_enemy_attack)

        self.finish_game_time[0] += time.time() - self.created_map
        self.created_map = 0

    def play_music(self):
        self.music_channel.set_volume(self.settings.music_volume)

        if not self.settings.play_music:
            self.music_channel.pause()
        else:
            self.music_channel.unpause()
        
        if self.player is not None:
            if self.player.paused_game:
                self.music_channel.pause()
            else:
                self.music_channel.unpause()
            
        if not self.music_channel.get_busy():
            self.set_musics()

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_gun_attack(self,gun,max_range,cost,):
        self.current_attack = GunsPlayer(self.player,cost, max_range, [self.visible_sprites,self.attack_sprites])

    def create_gun_enemy_attack(self, max_range,move_status,rect):
        direction = move_status.split('_')[0]  # Pegatt a direção em que o inimigo está se movendo
        player_group = pygame.sprite.GroupSingle(self.player)
        
        # Aqui, vamos ajustar a direção da bala, dependendo da direção do inimigo
        if direction == 'right':
            direction_bullet = pygame.math.Vector2(1, 0)
            spawn_pos = pygame.math.Vector2(rect.centerx + 40, rect.centery + 10)
        elif direction == 'left':
            direction_bullet = pygame.math.Vector2(-1, 0)
            spawn_pos = pygame.math.Vector2(rect.centerx - 40, rect.centery + 10)
        elif direction == 'up':
            direction_bullet = pygame.math.Vector2(0, -1)
            spawn_pos = pygame.math.Vector2(rect.centerx, rect.centery - 40)
        elif direction == 'down':
            direction_bullet = pygame.math.Vector2(0, 1)
            spawn_pos = pygame.math.Vector2(rect.centerx, rect.centery + 40)

        Bullet(self.enemy, spawn_pos, direction_bullet, max_range, [self.visible_sprites,self.attack_sprites],player_group, self.damage_player)

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
                layouts = ['boundary', 'objects', 'interactives', 'interactives_activated', 'interactives_chest_items', 'entities']
                self.music_folder = 'assets/musics/background'

                self.create_map(layouts)
            case LevelType.DUNGEON:
                layouts = ['boundary', 'interactives', 'entities']
                self.music_folder = 'assets/musics/background'

                self.create_map(layouts)
            case LevelType.CHESTDUNGEON:
                layouts = ['boundary', 'interactives', 'interactives_activated', 'interactives_chest_items', 'entities']
                self.music_folder = 'assets/musics/background'

                self.create_map(layouts)
            case LevelType.MAINMENU:
                self.music_folder = 'assets/musics/menu'

                self.is_main_menu = True
            case LevelType.HISTORY:
                self.music_folder = 'assets/musics/background'
                self.music_folder = ''

                self.is_history = True
            case LevelType.STORE:
                layouts = ['boundary', 'interactives', 'interactives_activated', 'entities']
                self.music_folder = 'assets/musics/background'

                self.create_map(layouts)

    def player_attack_collision(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                colision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if colision_sprites:
                    for target_sprite in colision_sprites:
                        if target_sprite.sprite_type == 'interactive':
                            if target_sprite.destructive == True:
                                target_sprite.destroyed_action([self.visible_sprites, self.interaction_sprites])
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damaged(self.player,attack_sprite.sprite_type)

    def interaction_collision(self, player: Player):
        collision_sprites = pygame.sprite.spritecollide(self.player_sprite.sprites()[0], self.interaction_sprites, False)

        if collision_sprites:
            for target_sprite in collision_sprites:
                if target_sprite.sprite_type == 'interactive':
                    target_sprite.special_function(player, self.visible_sprites.offset.x, self.visible_sprites.offset.y, self.inputs, self.graphics['interactives'], self.layouts, self)
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
        
        self.special_function()
        self.set_input_type(events)
        self.visible_sprites.custom_draw(self.player)
        self.interaction_collision(self.player)
        self.player_attack_collision()
        self.visible_sprites.enemy_update(self.player)
        self.hud.display(self.player)
        self.visible_sprites.update()

        if self.is_gameover_menu:
            self.gameover_menu.display_menu()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, map_path):
        super().__init__()

        self.save_window_size()

        self.offset = pygame.math.Vector2()

        if map_path != '':
            self.floor_surface = resize_image(map_path)
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