import pygame

pygame.init()
pygame.mixer.init()
# Константы

WIDTH = 1400
HEIGHT = 800
CELL_SIZE = 75
pygame.display.set_mode((WIDTH, HEIGHT))

# Цвета
BLACK = pygame.Color('black')
DARK_RED = pygame.Color('darkred')
WHITE = pygame.Color('white')
GRAY5 = pygame.Color('gray5')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')

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

# Звуки
CONTACT_LOST = pygame.mixer.Sound('data/sound/contact_lost.wav')
EXPLOSION = pygame.mixer.Sound('data/sound/explosion.wav')
FIRE_VLS = pygame.mixer.Sound('data/sound/FireVLS.wav')
NEW_CONTACT = pygame.mixer.Sound('data/sound/new_radar_contact.wav')
WEAPON_ACQUIRE = pygame.mixer.Sound('data/sound/weapon acquire.wav')
TAKEOFF = pygame.mixer.Sound('data/sound/air_takeoff.wav')
LANDING = pygame.mixer.Sound('data/sound/air_heading_back.wav')
ALL_SOUNDS = [CONTACT_LOST, EXPLOSION, FIRE_VLS, NEW_CONTACT, WEAPON_ACQUIRE, TAKEOFF, LANDING]

# Для меню паузы
MAIN_FONT = pygame.font.Font('data/font/Teletactile.ttf', 24)
SC_TEXT = MAIN_FONT.render('PAUSE', True, WHITE)
POS = SC_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2))
