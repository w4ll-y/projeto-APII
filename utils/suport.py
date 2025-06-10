from csv import reader, writer
from os import walk
from settings import ZOOM
import pygame

def import_csv_layout(path: str):
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')

        return list(layout)
    
def import_folder(path: str):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * ZOOM, image_surf.get_height() * ZOOM))

            surface_list.append(image_surf)

        return surface_list
    
def change_value_in_csv(path: str, pos: tuple, value: int):
    layout = []

    with open(path) as level_map:
        layout = list(reader(level_map, delimiter=','))
        layout[int(pos[0])][int(pos[1])] = str(value)

    with open(path, 'w') as level_map:
        file = writer(level_map)
        file.writerows(layout)
    

def resize_image(image_path: str):
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * ZOOM, image.get_height() * ZOOM))

    return image
