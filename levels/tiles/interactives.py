import pygame
from levels.tile import Tile
from entities.player import Player
from settings import *
from utils.suport import *
from utils.enums import InputType
from inputs.input_manager import InputManager

class Interactives(Tile):
    def __init__(self, pos: dict, original_pos: tuple, original_value: int, groups: list, sprite_type: str, surface = pygame.Surface((TILESIZE * ZOOM, TILESIZE * ZOOM)), activated: bool | None = None, inflate_ajust: tuple = (0, -5), hitbox_ajust: tuple = (0,0, 0, 0), destructive: bool = False, next_value: int = 0):
        super().__init__(pos, original_pos, original_value, groups, sprite_type, surface, activated, inflate_ajust, hitbox_ajust, destructive, next_value)

        self.hitbox2 = None

    def special_function(self, player: Player, offset_x, offset_y, input: InputManager, interactive_graphics):
        if self.original_value == 1:
            return self.chest_interaction(player, offset_x, offset_y, input, interactive_graphics)

    def chest_interaction(self, player: Player, offset_x, offset_y, input: InputManager, interactive_graphics):
        self.display_surface = pygame.display.get_surface()
        self.rect2 = self.image.get_rect(**self.pos)
        self.hitbox2 = self.rect2.inflate(20, 20)

        pos_x = self.pos['topleft'][0] - offset_x
        pos_y = self.pos['topleft'][1] - offset_y
        
        if self.hitbox2.colliderect(player.hitbox):
            key_graphic = resize_image(f'assets/graphics/hud/inputs/{'keyboard' if input.get_input().type == InputType.KEYBOARD else 'joystick'}/interact/{'default' if not player.interaction_button_pressed else 'pressed'}.png', 0.8)
            key_rect = key_graphic.get_rect(topleft = (pos_x + 4, pos_y - 50))

            self.display_surface.blit(key_graphic, key_rect)

        if player.interaction_button_pressed:
            self.image = interactive_graphics[self.next_value]
            self.activated = True

            change_value_in_csv('./storage/map/map_Interactives.csv', self.original_pos, self.next_value) #get the next tile Sprite
            change_value_in_csv('./storage/map/map_Interactives_Activated.csv', self.original_pos, 1) #save the activated state

            self.original_value = self.next_value

