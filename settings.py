# game setup
WIDTH    = 1280
HEIGHT   = 720
FPS      = 120
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 60
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15, 'graphic':'graphics/weapons/sword/full.png'}
}

# shield data
shield_data = {
	'shield': {'cooldown': 100, 'graphic': 'graphics/Objects/shield_icon.png'}
}

# magic
magic_data = {
	'heal': {'strength':20,'cost':7,'cooldown': 2000,'graphic':'graphics/particles/heal/frames/2.png'}
}

# enemy
monster_data = {
	'squid': {'health':30,'exp':20,'damage':5,'attack_type':'slash','attack_sound':'audio/attack/slash.wav','speed':3,'resistance':1,'attack_radius':80,'notice_radius':360},
	'spirit': {'health':6,'exp':15,'damage':6,'attack_type':'thunder','attack_sound':'audio/attack/fireball.wav','speed':4,'resistance':1 ,'attack_radius':60,'notice_radius':350},
	'bamboo': {'health':9,'exp':20,'damage':4,'attack_type':'leaf_attack','attack_sound':'audio/attack/slash.wav','speed':3,'resistance':1,'attack_radius':50,'notice_radius':300},
	'king_cheese': {'health':200,'exp':0,'damage':10,'attack_type':'claw','attack_sound':'audio/attack/claw.wav','speed':2,'resistance':0.2,'attack_radius':120,'notice_radius':400}
}