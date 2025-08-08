import pygame
from settings import *
from entities.entity import Entity
from os import walk
from utils.suport import resize_image

class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites):

        #geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #grafico
        self.import_graphics(enemy_name)
        self.move_status = 'idle'
        self.image = self.animations[self.move_status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.enemy_name = enemy_name
        enemy_info = ENEMY_DATA[self.enemy_name]
        self.health = enemy_info['health']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attacl_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

    def import_graphics(self,name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'assets/sprites/enemies/{name}/'
        for animaton in self.animations.keys():
            self.animations[animaton] = self.import_folder(main_path + animaton)

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)
    
    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attacl_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack':
           pass
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.move(self.speed)

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)

    def import_folder(self, path):
        surface_list = []
        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path+'/'+image
                image_surf = resize_image(full_path)
                surface_list.append(image_surf)
        return surface_list