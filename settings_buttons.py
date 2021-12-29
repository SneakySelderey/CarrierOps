import pygame
import pygame_gui
from Settings import *

"""Создание элементов окна настроек"""

settings_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

ok_text = MAIN_FONT.render('OK', True, WHITE)
rect = ok_text.get_rect()
rect.center = (WIDTH // 2, int(0.8 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 10, rect.y - 10, \
                                          rect.width + 20, rect.height + 20
OK_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='OK',
    manager=settings_manager
)

max_scr = max(WINDOW_SIZE, key=lambda x: len(f'{x[0]}{x[1]}'))
max_scr_text = MAIN_FONT.render(f'{max_scr[0]}X{max_scr[1]}', True, WHITE)
rect = max_scr_text.get_rect()
rect.center = (WIDTH // 4, int(0.6 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 10, rect.y - 10, \
                                          rect.width + 20, rect.height + 20
vars = [f'{i[0]}X{i[1]}' for i in WINDOW_SIZE]
DROP_DOWN_MENU = pygame_gui.elements.UIDropDownMenu(
    relative_rect=rect,
    manager=settings_manager,
    options_list=vars,
    starting_option=vars[0]
)

SETTINGS_ELEMENTS = {"OK": OK_BUTTON, "RESOLUTION": DROP_DOWN_MENU}
