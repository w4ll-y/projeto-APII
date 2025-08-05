import pygame
from utils.enums import OpenMapTileType
from settings import ZOOM,WEAPON_DATA   
from utils.suport import resize_image
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack,destroy_attack):
        super().__init__(groups)

        self.image = resize_image('assets/sprites/player/down_idle/player.png')

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, -5)

        self.import_player_asset()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        self.attack_button_pressed = False

        self.obstacle_sprites = obstacle_sprites

        self.stats = {
            'health': 150,
            'energy': 50,
            'attack': 8,
            'magic':  4,
            'speed': 5
        }

        self.actual_stats = {
            'health': 150,
            'energy': 50,
            'attack': 8,
            'magic':  4,
            'speed': 5
        }

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
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_n] and not self.attack_button_pressed:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack_button_pressed = True
                self.create_attack()
            elif not keys[pygame.K_n] and self.attack_button_pressed:
                self.attack_button_pressed = False

            if keys[pygame.K_m]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
            
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index+=1
                else:
                    self.weapon_index = 0

                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + "_idle"

            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0
                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        self.status = self.status.replace('_idle','_attack')
                    else:
                        self.status = self.status + '_attack'
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack','')

    def move(self, speed):
        if self.attacking:
            return None
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]
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
