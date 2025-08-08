import pygame
from utils.enums import OpenMapTileType
from settings import ZOOM,WEAPON_DATA, DEFAULT_STATS_VALUE, DEFAULT_ACTUAL_STATS_VALUE
from utils.suport import resize_image
from os import walk
from inputs.input_manager import InputManager
from entities.entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack,destroy_attack, inputs: InputManager):
        super().__init__(groups)

        self.inputs = inputs

        self.image = resize_image('assets/sprites/player/down_idle/player.png')

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, -5)

        self.import_player_asset()
        self.move_status = 'down'
        
        self.attacking = False
        self.scd_attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = self.get_weapon(self.weapon_index)
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        self.attack_button_pressed = False

        self.obstacle_sprites = obstacle_sprites

        self.stats = {
            'health': DEFAULT_STATS_VALUE * 3,
            'energy': DEFAULT_STATS_VALUE,
            'attack': DEFAULT_ACTUAL_STATS_VALUE,
            'magic':  DEFAULT_ACTUAL_STATS_VALUE,
            'speed': 5
        }

        self.actual_stats = {
            'health': DEFAULT_ACTUAL_STATS_VALUE * 6,
            'energy': DEFAULT_STATS_VALUE,
            'attack': DEFAULT_ACTUAL_STATS_VALUE,
            'magic':  DEFAULT_ACTUAL_STATS_VALUE,
            'speed': 5
        }

    def get_weapon(self, weapon_index: int):
        weapon_name = list(WEAPON_DATA.keys())[weapon_index]
        return WEAPON_DATA[weapon_name]

    def import_player_asset(self):
        character_path = 'assets/sprites/player/'
        self.animations = {'up':[], 'down': [], 'left':[], 'right': [],
                           'up_idle':[], 'down_idle': [], 'left_idle':[], 'right_idle': [],
                           'up_attack':[], 'down_attack': [], 'left_attack':[], 'right_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = self.import_folder(full_path)

    def import_folder(self, path):
        surface_list = []
        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path+'/'+image
                image_surf = resize_image(full_path)
                surface_list.append(image_surf)
        return surface_list
    
    def input(self):
        if not self.attacking:
            inputs = self.inputs.get_input()

            if inputs.is_walk_up():
                self.direction.y = -1
                self.move_status = 'up'
            elif inputs.is_walk_down():
                self.direction.y = 1
                self.move_status = 'down'
            else:
                self.direction.y = 0

            if inputs.is_walk_left():
                self.direction.x = -1
                self.move_status = 'left'
            elif inputs.is_walk_right():
                self.direction.x = 1
                self.move_status = 'right'
            else:
                self.direction.x = 0

            if inputs.is_frst_attacking() and not self.attack_button_pressed and self.weapon["energy_spent"] <= self.actual_stats["energy"]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack_button_pressed = True

                self.actual_stats["energy"] -= self.weapon["energy_spent"]
                self.create_attack()
            elif not inputs.is_frst_attacking() and self.attack_button_pressed:
                self.attack_button_pressed = False

            if inputs.is_scd_attacking():
                self.scd_attacking = True
                self.attack_time = pygame.time.get_ticks()
            
            if inputs.is_changing_weapon() and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index+=1
                else:
                    self.weapon_index = 0

                self.weapon = self.get_weapon(self.weapon_index)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.move_status and not 'attack' in self.move_status:
                self.move_status = self.move_status + "_idle"

            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0
                if not 'attack' in self.move_status:
                    if 'idle' in self.move_status:
                        self.move_status = self.move_status.replace('_idle','_attack')
                    else:
                        self.move_status = self.move_status + '_attack'
            else:
                if 'attack' in self.move_status:
                    self.move_status = self.move_status.replace('_attack','')

    def animate(self):
        animation = self.animations[self.move_status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.actual_stats['speed'])
