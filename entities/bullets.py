import pygame
from utils.suport import resize_image
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player, pos, direction, max_range, groups):
        super().__init__()
        self.add(*groups)

        self.image = resize_image('assets/sprites/guns/bullets/bullet.png')
        self.rect = self.image.get_rect(center=pos)

        self.direction = direction.normalize() if direction.length() != 0 else pygame.math.Vector2(0, 0)
        self.speed = player.gun['speed']

        self.start_pos = pygame.math.Vector2(pos)
        self.max_range = max_range

        self.sprite_type = 'gun'
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        print(self.rect)

        current_pos = pygame.math.Vector2(self.rect.center)
        if current_pos.distance_to(self.start_pos) >= self.max_range:
            self.kill()