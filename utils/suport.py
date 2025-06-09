from csv import reader
from os import walk
from settings import ZOOM
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')

        return list(layout)
    
def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * ZOOM, image_surf.get_height() * ZOOM))

            surface_list.append(image_surf)

        return surface_list
