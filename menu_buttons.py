from Settings import WIDTH, HEIGHT, WHITE, MAIN_FONT, get_bigger_rect
import pygame
import pygame_gui


"""Создание элементов основного меню"""

menu_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

quit_text = MAIN_FONT.render('QUIT TO DESKTOP', True, WHITE)
quit_rect = get_bigger_rect(quit_text.get_rect(center=(WIDTH // 2, int(0.75 * HEIGHT))), 20)
QUIT_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=quit_rect,
    text='QUIT TO DESKTOP',
    manager=menu_manager
)

settings_text = MAIN_FONT.render('SETTINGS', True, WHITE)
set_rect = get_bigger_rect(settings_text.get_rect(center=(WIDTH // 2, int(0.625 * HEIGHT))), 20)
SETTINGS_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=set_rect,
    text='SETTINGS',
    manager=menu_manager
)

new_campaign_text = MAIN_FONT.render('NEW CAMPAIGN', True, WHITE)
camp_rect = get_bigger_rect(new_campaign_text.get_rect(center=(WIDTH // 2, int(0.375 * HEIGHT))), 20)
NEW_GAME_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=camp_rect,
    text='NEW CAMPAIGN',
    manager=menu_manager
)

load_game_text = MAIN_FONT.render('LOAD SAVE', True, WHITE)
load_rect = get_bigger_rect(load_game_text.get_rect(center=(WIDTH // 2, int(0.5 * HEIGHT))), 20)
LOAD_SAVE_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=load_rect,
    text='LOAD SAVE',
    manager=menu_manager
)

# Все элемнты управления
MENU_ELEMENTS = {"QUIT": QUIT_BUTTON, "NEW_GAME": NEW_GAME_BUTTON,
                 "LOAD": LOAD_SAVE_BUTTON, "SETTINGS": SETTINGS_BUTTON}


class Title(pygame.sprite.Sprite):
    """Класс с названием игры"""
    def __init__(self, group):
        super().__init__(group)
        txt = MAIN_FONT.render('CARRIER OPERATIONS', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, HEIGHT // 5

    def update(self, pos):
        # сюда можно впихнуть пасхалку
        if self.rect.collidepoint(pos[0], pos[1]):
            pass
