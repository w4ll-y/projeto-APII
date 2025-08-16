import pygame
from utils.enums import OpenMapTileType
from settings import *
from utils.suport import resize_image
from os import walk
from inputs.input_manager import InputManager
from entities.entity import Entity
from ui.menu.pause import Pause

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack,destroy_attack, inputs: InputManager, pause: Pause, create_gun_attack):
        super().__init__(groups)

        self.inputs = inputs

        self.image = resize_image('assets/sprites/player/down_idle/player.png')

        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)
        self.hitbox = self.rect.inflate(-10, -5)

        self.import_player_asset()
        self.move_status = 'down'
        
        self.attacking = False
        self.scd_attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.getting_item = None
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = self.get_weapon(self.weapon_index)
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        self.attack_button_pressed = False
        self.interaction_button_pressed = False
        self.change_weapon_button_pressed = False

        #guns
        self.create_gun_attack = create_gun_attack
        self.guns_index = 0
        self.gun = self.get_guns(self.guns_index)
        self.can_switch_gun = True
        self.gun_switch_time = None

        self.obstacle_sprites = obstacle_sprites

        self.vulnerable = True
        self.hurt_time = None
        self.ivulnerability_duration = 500

        self.stats = {
            'health': DEFAULT_STATS_VALUE * 3,
            'energy': DEFAULT_STATS_VALUE,
            'attack': DEFAULT_ACTUAL_STATS_VALUE,
            'magic':  DEFAULT_ACTUAL_STATS_VALUE,
            'speed': 5
        }

        self.actual_stats = {
            'health': DEFAULT_ACTUAL_STATS_VALUE * 6,
            'energy': DEFAULT_ENERGY_STATS_VALUE * 10,
            'attack': DEFAULT_ACTUAL_STATS_VALUE,
            'magic':  DEFAULT_ACTUAL_STATS_VALUE,
            'speed': 5
        }

        self.weapon_attack_sound = pygame.mixer.Sound('assets/SEffects/brkn_wand_horizontal_sword.wav')
        self.weapon_attack_sound.set_volume(0.5)

        self.paused_game = False
        self.pause = pause
        self.pause.set_player(self)

    def get_weapon(self, weapon_index: int):
        weapon_name = list(WEAPON_DATA.keys())[weapon_index]
        return WEAPON_DATA[weapon_name]

    def get_guns(self, gun_index: int):
        gun_name = list(GUNS_DATA.keys())[gun_index]
        return GUNS_DATA[gun_name]

    def import_player_asset(self):
        character_path = 'assets/sprites/player/'
        self.animations = {'up':[], 'down': [], 'left':[], 'right': [],
                           'up_idle':[], 'down_idle': [], 'left_idle':[], 'right_idle': [],
                           'up_attack':[], 'down_attack': [], 'left_attack':[], 'right_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = self.import_folder_resize_image(full_path)

    def import_folder_resize_image(self, path):
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
                self.weapon_attack_sound.play()

                self.actual_stats["energy"] -= self.weapon["energy_spent"]
                self.create_attack()
            elif not inputs.is_frst_attacking() and self.attack_button_pressed:
                self.attack_button_pressed = False

            if inputs.is_scd_attacking() and self.scd_attacking == False:
                self.scd_attacking = True
                self.attack_time = pygame.time.get_ticks()
                gun = self.get_guns(self.guns_index)['name']
                strength = self.get_guns(self.guns_index)['damage']
                cost = self.get_guns(self.guns_index)['cost']
                max_range = self.get_guns(self.guns_index)['max_range']
                self.create_gun_attack(gun, max_range, cost)
            
            if inputs.is_changing_weapon() and self.can_switch_weapon and not self.change_weapon_button_pressed:
                self.can_switch_weapon = False
                self.change_weapon_button_pressed = True
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index+=1
                else:
                    self.weapon_index = 0

                self.weapon = self.get_weapon(self.weapon_index)
            elif not inputs.is_changing_weapon() and self.change_weapon_button_pressed:
                self.change_weapon_button_pressed = False

            if inputs.is_interacting() and not self.interaction_button_pressed:
                self.interaction_button_pressed = True
            elif not inputs.is_interacting() and self.interaction_button_pressed:
                self.interaction_button_pressed = False

            if inputs.is_pausing():
                self.paused_game = True

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

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self,attack_type):
        base_damage = self.stats['attack']
        weapon_damage = WEAPON_DATA[self.weapon_index]['damage']
        gun_damage = GUNS_DATA[self.guns_index]['damage']
        if attack_type == 'weapon':
            return base_damage + weapon_damage
        if attack_type == 'gun':
            return base_damage + gun_damage

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + WEAPON_DATA[self.weapon_index]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if self.scd_attacking:
            if current_time - self.attack_time >= self.attack_cooldown + GUNS_DATA[self.guns_index]['cooldown']:
                self.scd_attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.ivulnerability_duration:
                self.vulnerable = True


    def update(self):
        if self.paused_game:
            self.pause.display_menu()
            return

        if self.getting_item is not None:
            self.interaction_button_pressed = False
            self.move_status = 'down'
            self.get_status()
            self.animate()
            
            if pygame.time.get_ticks() >= self.getting_item['getted_time'] + 1200:
                self.move_status = self.getting_item['player_move_stats']
                self.getting_item['item_action'](self.getting_item['item_id'], self)
                self.getting_item = None

            return

        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.actual_stats['speed'])
