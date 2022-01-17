import pygame
import ctypes
import os
import sqlite3
from random import random
from collections import deque


def check(x, y, n, m):
    """Функция проверки попаданяи коорднаты в поле"""
    return 0 <= x < n and 0 <= y < m


def bfs(start, end):
    """Функция поиска в ширину в графе клеток поля"""
    path = []
    visited, queue = [start], deque([start])
    p = {}
    while queue:
        vertex = queue.popleft()
        if vertex == end:
            break
        for nr in GRAPH[vertex]:
            if nr not in visited and BOARD[nr[0]][nr[1]] != 'X':
                visited.append(nr)
                queue.append(nr)
                p[nr] = vertex
    if end in visited:
        to = end
        while to != start:
            path.append(to)
            to = p[to]
        path.reverse()
    return path


def find_free_space(start):
    """Функция поиска ближайшей свободной клетки"""
    visited, queue = [start], deque([start])
    while queue:
        vertex = queue.popleft()
        if BOARD[vertex[0]][vertex[1]] == '.':
            return vertex
        for nr in GRAPH[vertex]:
            if nr not in visited:
                visited.append(nr)
                queue.append(nr)


def get_pos_in_field(center, cell, top, left):
    """Возвращает положение объекта в сетке"""
    return [(center[0] - left) / cell, (center[1] - top) / cell]


def get_pos_in_coords(center, top, left):
    """Возвраащет положение объекта в системе координат"""
    return [left + center[0] * CELL_SIZE, top + center[1] * CELL_SIZE]


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


# Для параметров экрана
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
pygame.mixer.init()

# Группы спрайтосв
TO_DRAW = pygame.sprite.Group()
ANIMATED_SPRTIES = pygame.sprite.Group()
ALL_SPRITES_FOR_SURE = pygame.sprite.Group()
BASES_SPRITES = pygame.sprite.Group()
PLAYER_SPRITE = pygame.sprite.Group()
AI_SPRITE = pygame.sprite.Group()
PLAYER_MISSILES = pygame.sprite.Group()
PLAYER_AIRCRAFT = pygame.sprite.Group()
AI_MISSILES = pygame.sprite.Group()
AI_AIRCRAFT = pygame.sprite.Group()
ICONS_GROUP = pygame.sprite.Group()
RESOURCES_BASE = pygame.sprite.Group()
CARRIER_GROUP = pygame.sprite.Group()
BACKGROUND_MAP = pygame.sprite.Group()
MOVE_POINT_SPRITE = pygame.sprite.Group()
ALWAYS_UPDATE = pygame.sprite.Group()
BOARD = []
GRAPH = {}
EXPLOSION_GROUP = pygame.sprite.Group()
PARTICLES_GROUP = pygame.sprite.Group()
FRIENDLY_BASES = []
HOSTILE_BASES = []

# Числовые и булевые значения значения
AIR_SPEED = 2.5
MISSILE_SPEED = 2
FUEL_CONSUMPTION_SPEED = 2000
BASES_RATIO_R_A_M_O = 0.2, 0.2, 0.25, 0.35
BASE_TICKS = 240
GIVE_RESOURCE_TIME = 1000
PLAYER_SPEED = 1.5
AI_SPEED = 1
SPEEDS = {'PLAYER': 1.5, 'AI': 1.5, 'MISSILE': 2, 'AIRCRAFT': 2.5}
N = [(0, -1), (0, 1), (1, 0), (-1, 0)]
# N = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
NUM_OF_BASES = 10
PLAYER_START = None
AI_START = None
# Для подсчета результатов
LAUNCHED_MISSILES = 0
LAUNCHED_AIRCRAFT = 0
PLAYER_MISSILES_HIT = 0
AI_MISSILES_HIT = 0
BASES_CAPT_PLAYER = 0
BASES_CAPT_AI = 0

# Для экрана
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
TOP, LEFT = 0, 0
IS_FULLSCREEN = False
IS_PAUSE = True
pygame.display.set_mode((WIDTH, HEIGHT))

# Подлючение к БД
CONNECTION = sqlite3.connect('data/system/user_data.sqlite')
CONNECTION.execute("PRAGMA foreign_keys = ON")

# Events
MUSIC_END = pygame.USEREVENT + 1
FUEL_CONSUMPTION = pygame.USEREVENT + 2
UPDATE_ALL_SPRITES = pygame.USEREVENT + 3
UPDATE_ANIMATED_SPRITES = pygame.USEREVENT + 4
UPDATE_PARTICLES = pygame.USEREVENT + 5

# Цвета
BLACK = pygame.Color('black')
DARK_RED = pygame.Color('darkred')
WHITE = pygame.Color('white')
GRAY5 = pygame.Color('gray5')
DEEPSKYBLUE4 = pygame.Color('deepskyblue4')
GREY = pygame.Color('grey')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
WATER_COLORS = [pygame.Color('darkblue'), pygame.Color(62, 95, 138),
                pygame.Color(0, 47, 85), BLUE]
FIRE_COLORS = [RED, pygame.Color('yellow'), pygame.Color('orange'), GREY]
FADING = pygame.Color(0, 0, 0, 200)

# Изображения
GAME_ICON = pygame.image.load('data/img/icon.png').convert_alpha()
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
BASE_FRIENDLY = pygame.image.load('data/img/base_friendly.png').convert_alpha()
BASE_HOSTILE = pygame.image.load('data/img/base_hostile.png').convert_alpha()
BASE_NEUTRAL = pygame.image.load('data/img/base_neutral.png').convert_alpha()
MENU_BACKGROUND = pygame.image.load('data/img/menu_background.png').convert_alpha()
GAMEOVER_SCREEN = pygame.image.load('data/img/gameover_background.png').convert_alpha()
SETTINGS_BACKGROUND = pygame.image.load('data/img/settings_background.png').convert_alpha()
SAVE_LOAD_BACKGROUND = pygame.image.load('data/img/SAVE_LOAD_BACKGROUND.jpg').convert_alpha()
RESOURCE_BACKGROUND = pygame.image.load('data/img/resource_menu_background.jpg').convert_alpha()
SOLOMON_LAND = pygame.image.load('data/img/solomon_land.png').convert_alpha()
SOLOMON_WATER = pygame.image.load('data/img/solomon_water.png').convert_alpha()
SOLOMON_WATERMASK = pygame.image.load('data/img/solomon_watermask_negate.png').convert_alpha()
NORWEG_LAND = pygame.image.load('data/img/norwegian_sea_land.png').convert_alpha()
NORWEG_WATER = pygame.image.load('data/img/norwegian_sea_water.png').convert_alpha()
CHINA_LAND = pygame.image.load('data/img/south_china_sea_land.png').convert_alpha()
CHINA_WATER = pygame.image.load('data/img/south_china_sea_water.png').convert_alpha()
AIRCRAFT_FRIENDLY_SHEET = pygame.image.load('data/sheets/friendly_aircraft_sheet.png').convert_alpha()
AIRCRAFT_HOSTILE_SHEET = pygame.image.load('data/sheets/hostile_aircraft_sheet.png').convert_alpha()
PLAYER_CARRIER_SHEET = pygame.image.load('data/sheets/player_carrier_sheet.png').convert_alpha()
AI_CARRIER_SHEET = pygame.image.load('data/sheets/ai_carrier_sheet.png').convert_alpha()
PLAYER_MISSILE_SHEET = pygame.image.load('data/sheets/friendly_missile_sheet.png').convert_alpha()
HOSTILE_MISSILE_SHEET = pygame.image.load('data/sheets/hostile_missile_sheet.png').convert_alpha()
EXPLOSION_SHEET = pygame.image.load('data/sheets/explosion_sheet.png')
VICTORY = pygame.image.load('data/img/victory.jpg').convert_alpha()
LAND_CHECK_IMG = pygame.image.load('data/img/land_check.png').convert_alpha()
AI_MASK = pygame.image.load('data/img/ai_carrier.png').convert_alpha()
PLAYER_MASK = pygame.image.load('data/img/player_carrier.png').convert_alpha()

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
MAIN_BASE_DETECTION = pygame.mixer.Sound('data/sound/MainBaseDetected.wav')
MISSILE_DETECTION = pygame.mixer.Sound('data/sound/MissileWarning.wav')
SLIDE_EFFECTS = [TALKING, FOOTSTEPS]
ALL_EFFECTS = [CONTACT_LOST, EXPLOSION, FIRE_VLS, NEW_CONTACT, WEAPON_ACQUIRE,
               MISSILE_DETECTION, TAKEOFF, LANDING, CLOCK, TALKING, FOOTSTEPS,
               MORSE, MAIN_BASE_DETECTION]

# Музыка
MENU_MUSIC = os.listdir(os.getcwd() + '/data/music/menu/')
GAME_MUSIC = os.listdir(os.getcwd() + '/data/music/game/')
BATTLE_MUSIC = os.listdir(os.getcwd() + '/data/music/battle/')
GAMEOVER_MUSIC = os.listdir(os.getcwd() + '/data/music/gameover/')
VICTORY_MUSIC = os.listdir(os.getcwd() + '/data/music/win/')
GROUPS = [MENU_MUSIC, GAME_MUSIC, BATTLE_MUSIC, GAMEOVER_MUSIC]
ALL_MUSIC = [track for group in GROUPS for track in group]

# Шрифты
MAIN_FONT = pygame.font.Font('data/font/Teletactile.ttf', 24)

# Слайды пролога
files = os.listdir(os.getcwd() + '/data/slides/')
SLIDES = iter(sorted(files, key=lambda x: int(x[:x.find('.')])))
