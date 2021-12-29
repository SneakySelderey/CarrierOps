from Settings import *
import pygame
import pygame_gui

"""Создание элементов внутриигрового меню"""

game_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

resume_text = MAIN_FONT.render('RESUME', True, WHITE)
resume_rect = resume_text.get_rect()
resume_rect.center = (WIDTH // 2, HEIGHT // 6)
get_bigger_rect(resume_rect, 10)
RESUME_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=resume_rect,
    text='RESUME',
    object_id='option',
    manager=game_manager
)

