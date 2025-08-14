import pygame
from inputs.input_interface import InputInterface
from utils.enums import InputType

class Keyboard(InputInterface):
    def __init__(self):
        self.type = InputType.KEYBOARD
        self.keys = pygame.key.get_pressed()

    def is_walk_up(self) -> bool:
        return self.keys[pygame.K_w] or self.keys[pygame.K_UP]

    def is_walk_down(self) -> bool:
        return self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]
    
    def is_walk_left(self) -> bool:
        return self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]
    
    def is_walk_right(self) -> bool:
        return self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]

    def is_frst_attacking(self) -> bool:
        return self.keys[pygame.K_n]
    
    def is_scd_attacking(self) -> bool:
        return self.keys[pygame.K_m]

    def is_changing_weapon(self) -> bool:
        return self.keys[pygame.K_q]
    
    def is_interacting(self):
        return self.keys[pygame.K_e]
    
    def is_pausing(self):
        return self.keys[pygame.K_RETURN]
    
    def is_unpausing(self):
        return self.keys[pygame.K_ESCAPE] or self.keys[pygame.K_m]
    
    def is_selecting(self):
        return self.keys[pygame.K_n]