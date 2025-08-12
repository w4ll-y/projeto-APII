import pygame
from settings import *
from entities.entity import Entity
from os import walk
from utils.suport import resize_image, import_folder

class Enemy(Entity):
    def __init__(self, id, pos, groups, obstacle_sprites):

        #geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #grafico
        self.import_graphics(id)
        self.move_status = 'idle'
        self.image = self.animations[self.move_status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.id = id
        enemy_info = ENEMY_DATA[self.id]
        self.health = enemy_info['health']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

    def import_graphics(self, id):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'assets/sprites/enemies/{id}/'
        for animaton in self.animations.keys():
            self.animations[animaton] = import_folder(main_path + animaton)

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

        if distance <= self.attack_radius:
            self.move_status = 'attack'
        elif distance <= self.notice_radius:
            self.move_status = 'move'
        else:
            self.move_status = 'idle'

    def actions(self,player):
        if self.move_status == 'attack':
           pass
        elif self.move_status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.move_status]
        print(self.move_status)
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.move(self.speed)
        self.animate()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
