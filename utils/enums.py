from enum import Enum

class LevelType(Enum):
    MAINMENU = 'main_menu'
    OPENMAP = 'open_map'
    DUNGEON = 'dungeon'
    BOSSDUNGEON = 'boss_dungeon'
    CHESTDUNGEON = 'chest_dungeon'
    ENDGAMEDUNGEON = 'end_game_dungeon'
    HISTORY = 'history'
    CONFIGSCREEN = 'configscreen'
    GAMEOVER = 'game_over'
    STORE = 'store'

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
    REIS20 = 2
    REIS50 = 3