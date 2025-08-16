import pygame
from random import randint
from levels.tile import Tile
from entities.player import Player
from settings import *
from utils.suport import *
from utils.enums import InputType, DropType
from inputs.input_manager import InputManager
from levels.tiles.drop import Drop

class Interactives(Tile):
    def __init__(self, pos: dict, original_pos: tuple, original_value: int, groups: list, sprite_type: str, surface = pygame.Surface((TILESIZE * ZOOM, TILESIZE * ZOOM)), activated: bool | None = None, inflate_ajust: tuple = (0, -5), hitbox_ajust: tuple = (0,0, 0, 0), destructive: bool = False, next_value: int = 0):
        super().__init__(pos, original_pos, original_value, groups, sprite_type, surface, activated, inflate_ajust, hitbox_ajust, destructive, next_value)

        self.hitbox2 = None
        self.is_colliding = False

    def drop(self, groups: list):
        n = randint(1, 100)
        pos = {'center': (self.pos['topleft'][0] + 20, self.pos['topleft'][1] + 20)}

        if n <= 20:
            Drop(groups, DropType.HEALTH, pos)
        if 20 < n <= 40:
            Drop(groups, DropType.BULLET, pos)

    def special_function(self, player: Player, offset_x, offset_y, input: InputManager, interactive_graphics, chest_items_map):
        if self.original_value == 0:
            return self.cactus_interaction(player)
        if self.original_value == 1:
            return self.chest_interaction(player, offset_x, offset_y, input, interactive_graphics, chest_items_map)
        
    def cactus_interaction(self, player: Player):
        self.rect2 = self.image.get_rect(**self.pos)
        self.hitbox2 = self.rect2.inflate(20, 20)

        if self.hitbox.inflate(2, 2).colliderect(player.hitbox):
            self.is_colliding = True

        if self.hitbox2.colliderect(player.hitbox) and not self.hitbox.inflate(2, 2).colliderect(player.hitbox) and self.is_colliding == True:
            self.is_colliding = False

        if not self.is_colliding: player.actual_stats['health'] -= DEFAULT_ACTUAL_STATS_VALUE

    def chest_interaction(self, player: Player, offset_x, offset_y, input: InputManager, interactive_graphics, chest_items_map):
        display_surface = pygame.display.get_surface()
        self.rect2 = self.image.get_rect(**self.pos)
        self.hitbox2 = self.rect2.inflate(20, 20)

        pos_x = self.pos['topleft'][0] - offset_x
        pos_y = self.pos['topleft'][1] - offset_y
        
        if self.hitbox2.colliderect(player.hitbox):
            key_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if input.get_input().type == InputType.KEYBOARD else 'joystick'}/interact/default.png', 1)
            key_rect = key_graphic.get_rect(topleft = (pos_x + 4, pos_y - 50))

            display_surface.blit(key_graphic, key_rect)

        if player.interaction_button_pressed:
            self.image = interactive_graphics[self.next_value]
            self.activated = True

            change_value_in_csv('./storage/map/map_Interactives.csv', self.original_pos, self.next_value) #get the next tile Sprite
            change_value_in_csv('./storage/map/map_Interactives_Activated.csv', self.original_pos, 1) #save the activated state

            self.original_value = self.next_value

            #chest item logic
            item = chest_items_map[self.original_pos[0]][self.original_pos[1]]

            item_pos_x = display_surface.get_width() // 2 - 16
            item_pos_y = display_surface.get_height() // 2 - 64
            
            item_graphic = resize_image(f'assets/graphics/collectibles/chest_items/{str(item).rjust(2, '0')}.png', 1)
            item_rect = item_graphic.get_rect(topleft = (item_pos_x, item_pos_y))

            player.getting_item = {
                'getted_time': pygame.time.get_ticks(),
                'player_move_stats': player.move_status,
                'item_id': item,
                'item_graphic': item_graphic,
                'item_rect': item_rect,
                'item_action': self.chest_item_action
            }

    def chest_item_action(self, item_id: int, player: Player):
        if int(item_id) == 0:
            player.stats['health'] += DEFAULT_STATS_VALUE
            player.actual_stats['health'] = player.stats['health']
        if int(item_id) == 1:
            player.stats['bullets'] += 2
            player.actual_stats['bullets'] = player.stats['bullets']

