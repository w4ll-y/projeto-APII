import pygame
from utils.suport import resize_image
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player, pos, direction, max_range, groups , player_group, damage_player):
        super().__init__()
        self.add(*groups)

        self.player = player

        self.image = resize_image('assets/sprites/guns/bullets/bullet.png')
        self.rect = self.image.get_rect(center=pos)

        self.direction = direction.normalize() if direction.length() != 0 else pygame.math.Vector2(0, 0)
        self.speed = player.gun['speed']

        self.start_pos = pygame.math.Vector2(pos)
        self.max_range = max_range

        self.sprite_type = 'gun'

        if player.sprite_type == 'enemy': 
            self.player_group = player_group
            self.damage_player = damage_player

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        current_pos = pygame.math.Vector2(self.rect.center)
        if current_pos.distance_to(self.start_pos) >= self.max_range:
            self.kill()

        if self.player.sprite_type == 'enemy' and self.player_group:
            hit = pygame.sprite.spritecollideany(self, self.player_group)
            if hit:
                self.damage_player(ENEMY_DATA[0]['damage'], self.sprite_type)