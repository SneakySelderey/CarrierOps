from Settings import WIDTH, HEIGHT, WHITE, MAIN_FONT
import pygame
import pygame_gui

manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/settings.json')

quit_text = MAIN_FONT.render('QUIT TO DESKTOP', True, WHITE)
rect = quit_text.get_rect()
rect.center = (WIDTH // 2, int(0.75 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 20, rect.y - 20, \
                                          rect.width + 40, rect.height + 40
QUIT_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='QUIT TO DESKTOP',
    manager=manager
)

settings_text = MAIN_FONT.render('SETTINGS', True, WHITE)
rect = settings_text.get_rect()
rect.center = (WIDTH // 2, int(0.625 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 20, rect.y - 20, \
                                          rect.width + 40, rect.height + 40
SETTINGS_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='SETTINGS',
    manager=manager
)

new_campaign_text = MAIN_FONT.render('NEW CAMPAIGN', True, WHITE)
rect = new_campaign_text.get_rect()
rect.center = (WIDTH // 2, int(0.375 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 20, rect.y - 20, \
                                          rect.width + 40, rect.height + 40
NEW_GAME_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='NEW CAMPAIGN',
    manager=manager
)

load_game_text = MAIN_FONT.render('LOAD SAVE', True, WHITE)
rect = load_game_text.get_rect()
rect.center = (WIDTH // 2, int(0.5 * HEIGHT))
rect.x, rect.y, rect.width, rect.height = rect.x - 20, rect.y - 20, \
                                          rect.width + 40, rect.height + 40
LOAD_SAVE_BUTTON = pygame_gui.elements.UIButton(
    relative_rect=rect,
    text='LOAD SAVE',
    manager=manager
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
