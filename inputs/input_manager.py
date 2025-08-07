import pygame
from inputs.input_interface import InputInterface
from inputs.core.joystick import Joystick
from inputs.core.keyboard import Keyboard
from utils.enums import InputType

class InputManager():
    def __init__(self):
        self.input_type = InputType.JOYSTICK

        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            self.joystick = None
    
    def set_input_type(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.input_type = InputType.KEYBOARD
            elif event.type == pygame.JOYBUTTONDOWN:
                self.input_type = InputType.JOYSTICK

    def get_input(self) -> InputInterface:
        if self.input_type == InputType.JOYSTICK and self.joystick != None:
            return Joystick(self.joystick)
        else:
            return Keyboard()
