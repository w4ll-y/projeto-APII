from enum import Enum

class LevelType(Enum):
    MAINMENU = 0
    OPENMAP = 1
    DUNGEON = 2
    HISTORY = 3
    CONFIGSCREEN = 4

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
    ENERGY = 1
    COIN = 2