import pygame
import ctypes
import os
import sqlite3
from random import random


def random_resource_type():
    """Функция дял случайного выбора типа базы в зависимости от соотношения"""
    n = random()
    if 0 <= n < BASES_RATIO_R_A_M_O[0]:
        return 'repair'
    if BASES_RATIO_R_A_M_O[0] <= n < sum(BASES_RATIO_R_A_M_O[:2]):
        return 'aircraft'
    if sum(BASES_RATIO_R_A_M_O[:2]) <= n < sum(BASES_RATIO_R_A_M_O[:3]):
        return 'missile'
    return 'oil'


def get_bigger_rect(rect, d):
    """Функция для получения увеличенного прямоугольника"""
    rect.x, rect.y, rect.width, rect.height = \
        rect.x - d, rect.y - d, rect.width + d * 2, rect.height + d * 2
    return rect


def new_coords(x, y):
    """Функия для пересчета координат объекта при изменении разрешения.
    Принимет координату при старом разрешении"""
    return int(x / P_WIDTH * WIDTH), int(y / P_HEIGHT * HEIGHT)


def new_image_size(img):
    """Функия для изменения размера изображеня"""
    return pygame.transform.scale(img, (
            img.get_size()[0] * CELL_SIZE // 70,
            img.get_size()[1] * CELL_SIZE // 70))


def get_user_data():
    """Функция для получения информации из базы данных о сохранениях"""
    return {i[0]: i[1:] for i in CONNECTION.execute("""SELECT Saves.Title, 
Saves.Date, PathsOfSaves.Path FROM Saves INNER JOIN PathsOfSaves ON 
Saves.Path = PathsOfSaves.ID""").fetchall()}


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
pygame.mixer.init()

# Константы
ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES_FOR_SURE = pygame.sprite.Group()
BASES_SPRITES = pygame.sprite.Group()
PLAYER_SPRITE = pygame.sprite.Group()
TITLE_GROUP = pygame.sprite.Group()
GAMEOVER_GROUP = pygame.sprite.Group()
AI_SPRITE = pygame.sprite.Group()
PLAYER_MISSILES = pygame.sprite.Group()
PLAYER_AIRCRAFT = pygame.sprite.Group()
AI_MISSILES = pygame.sprite.Group()
AI_AIRCRAFT = pygame.sprite.Group()
ICONS_GROUP = pygame.sprite.Group()
RESOURCES_BASE = pygame.sprite.Group()
CARRIER_GROP = pygame.sprite.Group()
BACKGROUND_MAP = pygame.sprite.Group()
MOVE_POINT_SPRITE = pygame.sprite.Group()
FRIENDLY_BASES = []
HOSTILE_BASES = []
AIR_SPEED = 2
MISSILE_SPEED = 2
NUM_OF_MISSILES = 5
NUM_OF_AIRCRAFT = 3
OIL_VOLUME = 100
NUM_OF_REPAIR_PARTS = 0
BASE_NUM_OF_MISSILES = 0
BASE_NUM_OF_AIRCRAFT = 0
BASE_OIL_VOLUME = 0
BASE_NUM_OF_REPAIR_PARTS = 0
FUEL_CONSUMPTION_SPEED = 1000
BASES_RATIO_R_A_M_O = 0.2, 0.2, 0.25, 0.35
BASE_TICKS = 240
GIVE_RESOURCE_TIME = 1000
PLAYER_SPEED = 1.5
AI_SPEED = 1
NUM_OF_BASES = 10
PLAYER_START = None
AI_START = None
WINDOW_SIZE = [(3840, 2160), (1920, 1080), (1680, 1050), (1600, 1024),
               (1600, 900), (1440, 900), (1366, 768), (1280, 1024),
               (1280, 960), (1280, 800), (1280, 768), (1280, 720), (1152, 864),
               (1024, 768), (800, 600)]
try:
    WINDOW_SIZE = WINDOW_SIZE[WINDOW_SIZE.index(screensize)+3:]
except ValueError:
    WINDOW_SIZE = WINDOW_SIZE[WINDOW_SIZE.index((1280, 720)):]
WIDTH, HEIGHT = WINDOW_SIZE[0]
P_WIDTH, P_HEIGHT = 1600, 900
CELL_SIZE = WIDTH // 20
IS_FULLSCREEN = False
IS_PAUSE = True
pygame.display.set_mode((WIDTH, HEIGHT))

# Подлючение к БД
CONNECTION = sqlite3.connect('data/system/user_data.sqlite')
CONNECTION.execute("PRAGMA foreign_keys = ON")
USER_DATA = get_user_data()

# Events
MUSIC_END = pygame.USEREVENT + 1
FUEL_CONSUMPTION = pygame.USEREVENT + 2

# Цвета
BLACK = pygame.Color('black')
DARK_RED = pygame.Color('darkred')
WHITE = pygame.Color('white')
GRAY5 = pygame.Color('gray5')
DEEPSKYBLUE4 = pygame.Color('deepskyblue4')
GREY = pygame.Color('grey')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
FADING = pygame.Color(0, 0, 0, 200)

# Изображения
PLANE_ICON = pygame.transform.scale(pygame.image.load('data/img/plane.png'),
                                    (40, 40))
MISSILE_ICON = pygame.transform.scale(pygame.image.load(
    'data/img/missile.png'), (40, 40))
GEAR_ICON = pygame.transform.scale(pygame.image.load('data/img/gear.png'),
                                   (40, 40))
OIL_ICON = pygame.transform.scale(pygame.image.load('data/img/oil.png'),
                                   (40, 40))
PLAYER_BASE = pygame.image.load('data/img/base_player.png').convert_alpha()
AI_BASE = pygame.image.load('data/img/base_ai.png').convert_alpha()
PLAYER_IMAGE = pygame.image.load('data/img/Player_cursor.png').convert_alpha()
AI_IMAGE = pygame.image.load('data/img/AI_cursor.png').convert_alpha()
AI_HIDDEN = pygame.image.load('data/img/AI_cursor_hidden.png').convert_alpha()
BASE_FRIENDLY = pygame.image.load('data/img/base_friendly.png').convert_alpha()
BASE_HOSTILE = pygame.image.load('data/img/base_hostile.png').convert_alpha()
BASE_NEUTRAL = pygame.image.load('data/img/base_neutral.png').convert_alpha()
MISSILE_FRIENDLY = pygame.image.load('data/img/missile_friendly.png').convert_alpha()
MISSILE_HOSTILE = pygame.image.load('data/img/missile_hostile.png').convert_alpha()
AIRCRAFT_FRIENDLY = pygame.image.load('data/img/friendly_aircraft.png').convert_alpha()
MENU_BACKGROUND = pygame.image.load('data/img/menu_background.png').convert_alpha()
GAMEOVER_SCREEN = pygame.image.load('data/img/gameover_background.png').convert_alpha()
SETTINGS_BACKGROUND = pygame.image.load('data/img/settings_background.png').convert_alpha()
SAVE_LOAD_BACKGROUND = pygame.image.load('data/img/SAVE_LOAD_BACKGROUND.jpg').convert_alpha()
SOLOMON_LAND = pygame.image.load('data/img/solomon_land.png').convert_alpha()
SOLOMON_WATER = pygame.image.load('data/img/solomon_water.png').convert_alpha()
SOLOMON_WATERMASK = pygame.image.load('data/img/solomon_watermask.png').convert_alpha()

# Звуки
CONTACT_LOST = pygame.mixer.Sound('data/sound/contact_lost.wav')
EXPLOSION = pygame.mixer.Sound('data/sound/explosion.wav')
FIRE_VLS = pygame.mixer.Sound('data/sound/FireVLS.wav')
NEW_CONTACT = pygame.mixer.Sound('data/sound/new_radar_contact.wav')
WEAPON_ACQUIRE = pygame.mixer.Sound('data/sound/weapon acquire.wav')
TAKEOFF = pygame.mixer.Sound('data/sound/air_takeoff.wav')
LANDING = pygame.mixer.Sound('data/sound/air_heading_back.wav')
CLOCK = pygame.mixer.Sound('data/sound/Clock.wav')
TALKING = pygame.mixer.Sound('data/sound/talking.wav')
FOOTSTEPS = pygame.mixer.Sound('data/sound/Footsteps.wav')
MORSE = pygame.mixer.Sound('data/sound/morse.wav')
SLIDE_EFFECTS = [TALKING, FOOTSTEPS]
ALL_EFFECTS = [CONTACT_LOST, EXPLOSION, FIRE_VLS, NEW_CONTACT, WEAPON_ACQUIRE,
               TAKEOFF, LANDING, CLOCK, TALKING, FOOTSTEPS, MORSE]

# Музыка
MENU_MUSIC = os.listdir(os.getcwd() + '/data/music/menu/')
GAME_MUSIC = os.listdir(os.getcwd() + '/data/music/game/')
BATTLE_MUSIC = os.listdir(os.getcwd() + '/data/music/battle/')
GAMEOVER_MUSIC = os.listdir(os.getcwd() + '/data/music/gameover/')
GROUPS = [MENU_MUSIC, GAME_MUSIC, BATTLE_MUSIC, GAMEOVER_MUSIC]
ALL_MUSIC = [track for group in GROUPS for track in group]

# Шрифты
MAIN_FONT = pygame.font.Font('data/font/Teletactile.ttf', 24)

# Слайды пролога
files = os.listdir(os.getcwd() + '/data/slides/')
SLIDES = iter(sorted(files, key=lambda x: int(x[:x.find('.')])))
