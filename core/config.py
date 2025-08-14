import pygame
from utils.suport import *

class Config:
    def __init__(self):
        self.settings = read_settings()
        self.initial = True

        self.difficult = self.settings["difficult"]
        self.music_volume = self.settings["music_volume"]
        self.play_music = self.settings["play_music"]

    def compare_settings(self):
        data = read_settings()

        if self.settings != data:
            self.settings = data
            return True
        
        return False

    def run(self):
        if self.compare_settings() or self.initial:
            if self.settings["fullscreen_mode"]:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((self.settings["window_size"][0], self.settings["window_size"][1]), pygame.RESIZABLE)

            self.difficult = self.settings["difficult"]
            self.music_volume = self.settings["music_volume"]
            self.play_music = self.settings["play_music"]

            self.initial = False
