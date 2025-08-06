import pygame
from inputs.input_interface import InputInterface
from utils.enums import InputType

class Keyboard(InputInterface):
    def __init__(self):
        self.type = InputType.KEYBOARD
        self.keys = pygame.key.get_pressed()

    def is_walk_up(self) -> bool:
        return self.keys[pygame.K_w]

    def is_walk_down(self) -> bool:
        return self.keys[pygame.K_s]
    
    def is_walk_left(self) -> bool:
        return self.keys[pygame.K_a]
    
    def is_walk_right(self) -> bool:
        return self.keys[pygame.K_d]

    def is_frst_attacking(self) -> bool:
        return self.keys[pygame.K_n]
    
    def is_scd_attacking(self) -> bool:
        return self.keys[pygame.K_m]

    def is_changing_weapon(self) -> bool:
        return self.keys[pygame.K_q]