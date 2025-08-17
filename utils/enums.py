from enum import Enum

class LevelType(Enum):
    MAINMENU = 'main_menu'
    OPENMAP = 'open_map'
    DUNGEON = 'dungeon'
    HISTORY = 'history'
    CONFIGSCREEN = 'configscreen'

class OpenMapTileType(Enum):
    ROCK = 1

class BoundaryTyleTipe(Enum):
    SAND = 0
    GRASS = 1
    WATER = 2

class InputType(Enum):
    KEYBOARD = 0
    JOYSTICK = 1

class DropType(Enum):
    HEALTH = 0
    BULLET = 1
    COIN = 2