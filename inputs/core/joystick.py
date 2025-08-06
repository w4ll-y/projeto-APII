import pygame
from inputs.input_interface import InputInterface
from utils.enums import InputType

class Joystick(InputInterface):
    def __init__(self, joystick: pygame.joystick.Joystick):
        self.type = InputType.JOYSTICK
        self.joystick = joystick

    def is_walk_up(self) -> bool:
        return self.joystick.get_axis(1) > 0 or self.joystick.get_button(11)

    def is_walk_down(self) -> bool:
        return self.joystick.get_axis(1) < 0 or self.joystick.get_button(12)
    
    def is_walk_left(self) -> bool:
        return self.joystick.get_axis(0) < 0 or self.joystick.get_button(13)
    
    def is_walk_right(self) -> bool:
        return self.joystick.get_axis(0) > 0 or self.joystick.get_button(14)

    def is_frst_attacking(self) -> bool:
        return self.joystick.get_button(0)
    
    def is_scd_attacking(self) -> bool:
        return self.joystick.get_button(2)

    def is_changing_weapon(self) -> bool:
        return self.joystick.get_button(9)