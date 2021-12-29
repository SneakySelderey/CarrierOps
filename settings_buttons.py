import pygame
import pygame_gui
from Settings import *

"""Создание элементов окна настроек"""

settings_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

settings_text = pygame.font.Font('data/font/Teletactile.ttf', 36).render(
    'SETTINGS', True, WHITE)
setting_rect = settings_text.get_rect()
setting_rect.center = (WIDTH // 2, HEIGHT // 8)
SETTINGS_LABEL = pygame_gui.elements.UILabel(
    relative_rect=setting_rect,
    text='SETTINGS',
    manager=settings_manager,
    object_id="settings"
)

res_text = MAIN_FONT.render('RESOLUTION', True, WHITE)
res_rect = res_text.get_rect()
res_rect.topleft = (WIDTH // 5, int(0.5 * HEIGHT))
RESOLUTION_LABEL = pygame_gui.elements.UILabel(
    relative_rect=res_rect,
    text='RESOLUTION',
    manager=settings_manager,
    object_id='option'
)

volume_text = MAIN_FONT.render('VOLUME', True, WHITE)
vol_rect = volume_text.get_rect()
vol_rect.topleft = (WIDTH // 5, int(0.2 * HEIGHT))
VOLUME_LABEL = pygame_gui.elements.UILabel(
    relative_rect=vol_rect,
    text='VOLUME',
    manager=settings_manager,
    object_id='option'
)

music_text = MAIN_FONT.render('MUSIC', True, WHITE)
music_rect = music_text.get_rect()
music_rect.topleft = (WIDTH // 5, int(0.3 * HEIGHT))
MUSIC_LABEL = pygame_gui.elements.UILabel(
    relative_rect=music_rect,
    text='MUSIC',
    manager=settings_manager,
    object_id='option'
)

effects_text = MAIN_FONT.render('EFFECTS', True, WHITE)
effects_rect = effects_text.get_rect()
effects_rect.topleft = (WIDTH // 5, int(0.37 * HEIGHT))
EFFECTS_LABEL = pygame_gui.elements.UILabel(
    relative_rect=effects_rect,
    text='EFFECTS',
    manager=settings_manager,
    object_id='option'
)


ok_text = MAIN_FONT.render('OK', True, WHITE)
ok_rect = ok_text.get_rect()
ok_rect.center = (WIDTH // 2, int(0.9 * HEIGHT))
ok_rect.x, ok_rect.y, ok_rect.width, ok_rect.height = \
    ok_rect.x - 10, ok_rect.y - 10, ok_rect.width + 20, ok_rect.height + 20
OK_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=ok_rect,
    text='OK',
    manager=settings_manager
)

max_scr = max(WINDOW_SIZE, key=lambda x: len(f'{x[0]}{x[1]}'))
max_scr_text = MAIN_FONT.render(f'{max_scr[0]}X{max_scr[1]}', True, WHITE)
rect = max_scr_text.get_rect()
rect.topleft = (WIDTH // 5 + 15, int(0.6 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 15, rect.y - 15, \
                                          rect.width + 30, rect.height + 30
vars = [f'{i[0]}X{i[1]}' for i in WINDOW_SIZE]
DROP_DOWN_MENU = pygame_gui.elements.UIDropDownMenu(
    relative_rect=rect,
    manager=settings_manager,
    options_list=vars,
    starting_option=vars[0]
)

music_bar_rect = pygame.Rect(music_rect.topright[0] + 40, music_rect.topright[1], WIDTH // 6, music_rect.height)
MUSIC_BAR = pygame_gui.elements.UIHorizontalSlider(
    manager=settings_manager,
    value_range=(1, 10),
    start_value=10,
    relative_rect=music_bar_rect
)

effect_bar_rect = pygame.Rect(effects_rect.topright[0] + 40, effects_rect.topright[1], WIDTH // 6, effects_rect.height)
EFFECT_BAR = pygame_gui.elements.UIHorizontalSlider(
    manager=settings_manager,
    value_range=(1, 10),
    start_value=10,
    relative_rect=effect_bar_rect
)


SETTINGS_ELEMENTS = {"OK": OK_BUTTON, "RESOLUTION": DROP_DOWN_MENU,
                     "MUSIC": MUSIC_BAR, "EFFECTS": EFFECT_BAR}
