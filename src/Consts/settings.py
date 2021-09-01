# -------------------COLORS------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
NO_COLOR = (255, 255, 255, 128)
DEBUGGING_COLOR = (100, 100, 100)
# ------------------WINDOW SIZE------------------------
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
# -----------------GAME LOOP SETTINGS----------------------
FPS = 500
# -----------------CAMERA SETTINGS----------------------
CAMERA_SPEED = 0
# -----------------MAP SETTINGS------------------------
MAP_HEIGHT = 3000
MAP_WIDTH = 3000
# -----------------PLAYERS SETTINGS----------------------
PLAYER_SPEED = 500
PLAYER_HEALTH = 100
PLAYER_POWER = 20
# -----------------ENEMY SETTINGS-------------------
BASE_ENEMY_SPEED = 300
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
# --------------------BULLET SETTINGS----------------
BULLET_BASE_SPEED = 500
BULLET_BASE_POWER = 10
BULLET_BASE_HEALTH = 1  # after it hits something he will die
BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_TIME_TO_LIVE = 3
# --------------------GUNS SETTINGS-----------------
# PISTOL---------------------------------------
PISTOL_POWER_MULTIPLIER = 10
PISTOL_SPEED_MULTIPLIER = 3
PISTOL_HEALTH_MULTIPLIER = 1000
PISTOL_TIME_BETWEEN_SHOTS = 0.01
PISTOL_MAGAZINE_SIZE = 5
PISTOL_PRICE = 10
# SHOTGUN------------------------------------------
SHOTGUN_POWER_MULTIPLIER = 3
SHOTGUN_SPEED_MULTIPLIER = 3
SHOTGUN_HEALTH_MULTIPLIER = 1
SHOTGUN_TIME_BETWEEN_SHOTS = 0.5
SHOTGUN_MAGAZINE_SIZE = 30
SHOTGUN_BULLET_NUMBER = 7
SHOTGUN_ANGLE_CHANGE = 3
SHOTGUN_PRICE = 20

# RIFLE---------------------------------------------
RIFLE_POWER_MULTIPLIER = 3
RIFLE_SPEED_MULTIPLIER = 3
RIFLE_HEALTH_MULTIPLIER = 1
RIFLE_TIME_BETWEEN_SHOTS = 0.05
RIFLE_MAGAZINE_SIZE = 30
RIFLE_PRICE = 30

# SNIPER----------------------------------------------
SNIPER_POWER_MULTIPLIER = 10
SNIPER_SPEED_MULTIPLIER = 3
SNIPER_HEALTH_MULTIPLIER = 3
SNIPER_TIME_BETWEEN_SHOTS = 1
SNIPER_MAGAZINE_SIZE = 30
SNIPER_PRICE = 40
# -----------------TILE SETTINGS----------------------
TILE_HEIGHT = MAP_HEIGHT / 10  # there are 10 tiles
TILE_WIDTH = MAP_WIDTH / 10  # there are 10 tiles
# ------------------FONTS----------------------------
COSMIC_SANS_FONT = 'Comic Sans MS'
# -------------------MOUSE SIZE---------------------
MOUSE_WIDTH = 5
MOUSE_HEIGHT = 5
# ------------------EVENTS-------------------------
MOUSE_LEFT_CLICK = "left click"
MOUSE_LEFT_CLICK_CORDINENETS = "left click with coordinates" #Returns the x and y pos of the mouse when got clicked
MOUSE_LEFT_PRESSED = "mouse left pressed"
WORLD_ADD_OBJECT = "add object"
WORLD_REMOVE_OBJECT = "remove object"
KEY_DOWN = "key down:"
GO_TO_MENU_STATE = "to menu"
GO_TO_GAME_STATE = "to game"
SHOP_MENU = "shop menu"
BUY_GUN = "buy gun"
# ------------------IMAGES-----------------------
PLAYER_IMAGE = "..\\images\\sprites\\solider.png"
ONLINE_PLAYER_IMAGE = "..\\images\\sprites\\online_player.png"
PISTOL_IMAGE = "..\\images\\sprites\\gun.png"
SHOTGUN_IMAGE = "..\\images\\sprites\\shotgun.png"
RIFLE_IMAGE = "..\\images\\sprites\\rifle.png"
SNIPER_IMAGE = "..\\images\\sprites\\sniper.png"
BULLET_IMAGE = "..\\images\\sprites\\bullet.png"
BASIC_ENEMY_IMAGE = "..\\images\\sprites\\basic_enemy.png"
COIN_IMAGE = "..\\images\\sprites\\coin.png"
AMMO_BOX_IMAGE = "..\\images\\sprites\\ammo_box.png"
# ------------------MENUS-----------------------
STARTING_MENU = "start menu"
MATCHMAKING_MENU = "matchmaking menu"
SETTINGS_MENU = "settings menu"
SETTINGS2_MENU = "settings2 menu"
WON_MENU = "won menu"
LOST_MENU = "lost menu"
RESET_GAME = "reset game"
# ------------------ITEMS--------------------
STARTING_COINS = 30
STARTING_AMMO = 200
# ------------------NETWORK-----------------
IP = "127.0.0.1"
PORT = 2222
NUMBER_OF_PLAYERS_IN_GAME = 2
# MASSAGES-----------------
NETWORK_PLAYER_POS = "player pos"
NETWORK_GUN_ROTATION = "gun rotation"
NETWORK_SPAWNER_POS = "spawner pos"
NETWORK_MOUSE_LEFT_CLICK = "left click"
NETWORK_NEW_GUN = "new gun"
NETWORK_MOUSE_LEFT_PRESSED = "left press"
NETWORK_KEYDOWN = "key down"
NETWORK_PLAYER_WON = "i won"
