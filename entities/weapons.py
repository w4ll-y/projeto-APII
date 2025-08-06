import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = player.move_status.split('_')[0]
        
        full_path = f'assets/sprites/weapons/{player.weapon["name"]}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,18)) #se quiser alinhas o sprite da arma é só mudar o valor do vector2
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,18))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,10))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,10))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)
        