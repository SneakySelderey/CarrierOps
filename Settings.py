import pygame
import ctypes


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
pygame.mixer.init()
# Константы

WINDOW_SIZE = [(3840, 2160), (1920, 1080), (1680, 1050), (1600, 1024), (1600, 900),
               (1440, 900), (1366, 768), (1280, 1024), (1280, 960),
               (1280, 800), (1280, 768), (1280, 720), (1152, 864),
               (1024, 768), (800, 600)]
try:
    WINDOW_SIZE = WINDOW_SIZE[WINDOW_SIZE.index(screensize) + 0:]
except ValueError:
    WINDOW_SIZE = WINDOW_SIZE[WINDOW_SIZE.index((1280, 720)):]
WIDTH, HEIGHT = WINDOW_SIZE[0]
CELL_SIZE = WIDTH // 15
pygame.display.set_mode((WIDTH, HEIGHT))

# Цвета
BLACK = pygame.Color('black')
DARK_RED = pygame.Color('darkred')
WHITE = pygame.Color('white')
GRAY5 = pygame.Color('gray5')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
FADING = pygame.Color(0, 0, 0, 200)

# Изображения
PLAYER_IMAGE = pygame.image.load('data/img/Player_cursor.png')
AI_IMAGE = pygame.image.load('data/img/AI_cursor.png')
AI_HIDDEN = pygame.image.load('data/img/AI_cursor_hidden.png')
BASE_FRIENDLY = pygame.image.load('data/img/base_friendly.png')
BASE_HOSTILE = pygame.image.load('data/img/base_hostile.png')
BASE_NEUTRAL = pygame.image.load('data/img/base_neutral.png')
MISSILE_FRIENDLY = pygame.image.load('data/img/missile_friendly.png')
MISSILE_HOSTILE = pygame.image.load('data/img/missile_hostile.png')
AIRCRAFT_FRIENDLY = pygame.image.load('data/img/friendly_aircraft.png')
MENU_BACKGROUND = pygame.image.load('data/img/menu_background.png')
GAMEOVER_SCREEN = pygame.image.load('data/img/gameover_background.png')
SETTINGS_BACKGROUND = pygame.image.load('data/img/settings_background.png')

# Звуки
CONTACT_LOST = pygame.mixer.Sound('data/sound/contact_lost.wav')
EXPLOSION = pygame.mixer.Sound('data/sound/explosion.wav')
FIRE_VLS = pygame.mixer.Sound('data/sound/FireVLS.wav')
NEW_CONTACT = pygame.mixer.Sound('data/sound/new_radar_contact.wav')
WEAPON_ACQUIRE = pygame.mixer.Sound('data/sound/weapon acquire.wav')
SUB_SUNK = pygame.mixer.Sound('data/sound/SubSunk.wav')
TAKEOFF = pygame.mixer.Sound('data/sound/air_takeoff.wav')
LANDING = pygame.mixer.Sound('data/sound/air_heading_back.wav')
ALL_SOUNDS = [CONTACT_LOST, EXPLOSION, FIRE_VLS, NEW_CONTACT, WEAPON_ACQUIRE, TAKEOFF, LANDING, SUB_SUNK]

# Шрифты
MAIN_FONT = pygame.font.Font('data/font/Teletactile.ttf', 24)
