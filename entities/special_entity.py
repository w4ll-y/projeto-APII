import pygame
from entities.entity import Entity
from utils.suport import import_folder_resize_image

class SpecialEntity(Entity):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.animations = import_folder_resize_image('assets/sprites/special_entity')

        self.sprite_type = 'special'

        self.frame_index = 0
        self.image = self.animations[self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)  

        self.hitbox.height = 100

    def animate(self):
        animation = self.animations
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):      
        self.animate()