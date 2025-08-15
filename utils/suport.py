from csv import reader, writer
from os import walk, listdir, path, remove
from settings import ZOOM
import shutil
import json
import pygame

def import_csv_layout(path: str):
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')

        return list(layout)
    
def import_folder_files(path: str):
    for _, __, files in walk(path):
        files.sort()
        files = map(lambda x: path + '/' + x, files)
        
        return list(files)
    
def import_folder_resize_image(path: str, zoom_modificator: float = 1):
    for _, __, img_files in walk(path):
        img_files.sort()
        surface_list = [0 for _ in range(len(img_files))]

        for index, image in enumerate(img_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * ZOOM * zoom_modificator, image_surf.get_height() * ZOOM * zoom_modificator))

            surface_list[index] = image_surf 

        return surface_list
    
def change_value_in_csv(path: str, pos: tuple, value: int):
    layout = []

    with open(path) as level_map:
        layout = list(reader(level_map, delimiter=','))
        layout[int(pos[0])][int(pos[1])] = str(value)

    with open(path, 'w', newline='', encoding='utf-8') as level_map:
        file = writer(level_map)
        file.writerows(layout)
    

def resize_image(image_path: str, zoom_modificator: float = 1):
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * ZOOM * zoom_modificator, image.get_height() * ZOOM * zoom_modificator))

    return image

def reset_game():
    origin = "storage/map/backup"
    destination = "storage/map"

    for file_name in listdir(destination):
        origin_way = path.join(destination, file_name)

        if path.isfile(origin_way):
            remove(path.abspath(origin_way))

    for file_name in listdir(origin):
        origin_way = path.join(origin, file_name)

        if path.isfile(origin_way):
            extensao = path.splitext(file_name)[1]
            
            base_name = path.splitext(file_name)[0][:-7]
            new_name = f"{base_name}{extensao}"
            
            destination_way = path.join(destination, new_name)
            
            shutil.copy2(origin_way, destination_way)

def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def read_settings():
    return read_json("data/settings.json")

def change_settings_value(key, new_value):
    data = read_settings()
    data[key] = new_value

    with open("data/settings.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def obj_inflate_ajust(object_id: int):
    if object_id == 0:
        return (0, -20)
    elif object_id == 11:
        return (-160, 0)
    elif object_id == 12:
        return (-50, -60)
        
    return (0, -5)

def obj_hitbox_ajust(object_id: int):
    if object_id == 1 or object_id == 7:
        return (-31, 0, -31, 0)
    elif object_id == 2 or object_id == 8:
        return (-32, 0, 64, 0)
    elif object_id == 5:
        return (-32, 25, 64, -25)
    elif object_id == 9:
        return (32, -30, -32, -30)
    elif object_id == 11:
        return (0, -80, 0, -80)
    elif object_id == 15:
        return (0, -40, 0, -40)
        
    return (0, 0, 0, 0)

def is_icv_destructive(icv_id: int):
    if icv_id in [0, 3, 4]:
        return True
    
    return False

def icv_next_value(icv_id: int):
    if icv_id in [1]:
        return icv_id + 1
    
    return icv_id