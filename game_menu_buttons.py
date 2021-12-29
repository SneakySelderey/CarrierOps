from Settings import *
import pygame
import pygame_gui
from menu_buttons import load_rect, set_rect, quit_rect

"""Создание элементов внутриигрового меню"""

game_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

resume_text = MAIN_FONT.render('RESUME', True, WHITE)
resume_rect = get_bigger_rect(resume_text.get_rect(center=(WIDTH // 2, int(0.250 * HEIGHT))), 20)
RESUME_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=resume_rect,
    text='RESUME',
    manager=game_manager
)

menu_text = MAIN_FONT.render('MAIN MENU', True, WHITE)
menu_rect = get_bigger_rect(menu_text.get_rect(center=(WIDTH // 2, int(0.375 * HEIGHT))), 20)
MENU_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=menu_rect,
    text='MAIN MENU',
    manager=game_manager
)

LOAD_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=load_rect,
    text="LOAD SAVE",
    manager=game_manager,
)

SETTING_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=set_rect,
    text='SETTINGS',
    manager=game_manager,
)


QUIT_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=quit_rect,
    text='QUIT TO DESKTOP',
    manager=game_manager,
)

IN_GAME_ELEMENTS = {"RESUME": RESUME_BUTTON, "MENU": MENU_BUTTON,
                    "LOAD": LOAD_BUTTON, "SETTINGS": SETTING_BUTTON,
                    "QUIT": QUIT_BUTTON}
