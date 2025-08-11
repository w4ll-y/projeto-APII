WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 32
ZOOM = 1.5

DEFAULT_STATS_VALUE = 50 #The player's default stats must be a multiple of 50
DEFAULT_ACTUAL_STATS_VALUE = 25 #The actual player stats must be a multiple of 25

HEALTH_HEIGHT = 64
HEALTH_WIDTH = 64

BAR_HEIGHT = 18
DEFAUTL_BAR_WIDTH = 25

ITEM_BOX_SIZE = 120

UI_BG_COLOR = '#1D1D1D'
UI_BORDER_COLOR = '#0A0A0A'

ENERGY_BORDER_COLOR = '#4b726e'
ENERGY_COLOR = '#8caba1'

WORLD_MAP = [[''] * 100 for _ in range(100)]
WORLD_MAP[72][42] = 'p'

WEAPON_DATA = {
    1: {'name': 'facao', 'cooldown': 100 , 'damage': 15, 'graphic': 'assets/sprites/weapons/facao/right.png', 'energy_spent': 0},
    2: {'name': 'espingarda', 'cooldown': 100 , 'damage': 30, 'graphic': 'assets/sprites/weapons/espingarda/right.png', 'energy_spent': 10}
}

ENEMY_DATA = {
    0: {'health': 40, 'damage': 50 , 'attack_type': 'slash', 'attack_sound': None, 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    2: {'health': 40, 'damage': 50 , 'attack_type': 'slash', 'attack_sound': None, 'speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360}
}