from Settings import *
import pygame_gui

"""Создание элементов экрана поражения"""

gameover_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')


menu_text = MAIN_FONT.render('MAIN MENU', True, WHITE)
rect = get_bigger_rect(menu_text.get_rect(center=(WIDTH // 2, int(0.625 * HEIGHT))), 20)
MAIN_MENU_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='MAIN MENU',
    manager=gameover_manager
)

quit_text = MAIN_FONT.render('QUIT TO DESKTOP', True, WHITE)
rect = get_bigger_rect(quit_text.get_rect(center=(WIDTH // 2, int(0.75 * HEIGHT))), 20)
QUIT_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='QUIT TO DESKTOP',
    manager=gameover_manager
)

GAMEOVER_ELEMENTS = {"QUIT": QUIT_BUTTON, "MENU": MAIN_MENU_BUTTON}


class BasesLost(pygame.sprite.Sprite):
    """Класс с надписью о том, что все базы захвачены противником"""
    def __init__(self, group):
        super().__init__(group)
        txt = MAIN_FONT.render("GAME OVER. YOU'VE LOST ALL BASES", True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, int(0.375 * HEIGHT)