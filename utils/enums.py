from enum import Enum

class LevelType(Enum):
    OPENMAP = 1
    DUNGEON = 2

class OpenMapTileType(Enum):
    ROCK = 1

class BoundaryTyleTipe(Enum):
    SAND = 0
    GRASS = 1
    WATER = 2