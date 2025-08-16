WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 32
ZOOM = 1.5

HEALTH_HEIGHT = 64
HEALTH_WIDTH = 64

BAR_HEIGHT = 18
DEFAUTL_BAR_WIDTH = 25

ITEM_BOX_SIZE = 120

UI_BG_COLOR = '#1D1D1D'
UI_BORDER_COLOR = '#0A0A0A'

ENERGY_BORDER_COLOR = '#4b726e'
ENERGY_COLOR = '#8caba1'

WEAPON_DATA = {
    0: {'name': 'faca', 'cooldown': 100 , 'damage': 10, 'graphic': 'assets/sprites/weapons/faca/right.png'},
    1: {'name': 'facao', 'cooldown': 100 , 'damage': 15, 'graphic': 'assets/sprites/weapons/facao/right.png'}
}

GUNS_DATA = {
    0:{'name': 'espingarda', 'cost': 2, 'damage': 50, 'speed': 20, 'max_range': 200, 'cooldown': 150 , 'graphic': 'assets/sprites/guns/espingarda/right.png' },
    1:{'name': 'revolver', 'cost': 1, 'damage': 20, 'speed': 20, 'max_range': 500, 'cooldown': 100 , 'graphic': 'assets/sprites/guns/revolver/right.png' }
}

ENEMY_DATA = {
    0: {'health': 40, 'damage': DEFAULT_ACTUAL_STATS_VALUE, 'attack_type': 'slash', 'attack_sound': None, 'speed': 2, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 360},
    2: {'health': 100, 'damage': DEFAULT_ACTUAL_STATS_VALUE * 2, 'attack_type': 'slash', 'attack_sound': None, 'speed': 2, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 360}
}