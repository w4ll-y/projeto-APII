import pygame
from settings import *
from utils.suport import resize_image
from entities.bullets import Bullet

class GunsPlayer(pygame.sprite.Sprite):
    def __init__(self, player, cost, max_range, groups):
        super().__init__(groups)

        self.sprite_type = 'weapon'
        direction = player.move_status.split('_')[0]
        full_path = f'assets/sprites/guns/{player.gun["name"]}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

    #se quiser alinhar o sprite da arma é só mudar o valor do vector2
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-15,15)) 
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(15,15))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,0))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)

    #se quiser alinhar o sprite da bala é só mudar o valor dps do + ou -
        if player.actual_stats['energy'] >= cost:
            player.actual_stats['energy'] -= cost

            if player.move_status.split('_')[0] == 'right':
                direction_bullet = pygame.math.Vector2(1, 0)
                spawn_pos = pygame.math.Vector2(player.rect.centerx + 40, player.rect.centery + 10)
            elif player.move_status.split('_')[0] == 'left':
                direction_bullet = pygame.math.Vector2(-1, 0)
                spawn_pos = pygame.math.Vector2(player.rect.centerx - 40, player.rect.centery + 10)
            elif player.move_status.split('_')[0] == 'up':
                direction_bullet = pygame.math.Vector2(0, -1)
                spawn_pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery - 40)
            else:
                direction_bullet = pygame.math.Vector2(0, 1)
                spawn_pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery + 40)

            print(direction_bullet)
            Bullet(player,spawn_pos, direction_bullet, max_range, groups)
