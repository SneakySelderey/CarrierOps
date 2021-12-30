from Settings import WIDTH, HEIGHT, WHITE, MAIN_FONT, WINDOW_SIZE
import pygame
import pygame_gui

"""Создание элементов основного меню"""


def get_bigger_rect(rect, d):
    """Функция для получения увеличенного прямоугольника"""
    rect.x, rect.y, rect.width, rect.height = \
        rect.x - d, rect.y - d, rect.width + d * 2, rect.height + d * 2
    return rect


class Label(pygame_gui.elements.UILabel):
    """Класс для метки"""
    def __init__(self, font_size, title, x, y, manager, obj_id=None,
                 pos='center'):
        """Инициализация. Принимает размер шрифта, заголовок, положегние,
        менеджер, id, и часть прямоугольника, которую задают x и y"""
        text = pygame.font.Font('data/font/Teletactile.ttf', font_size).render(
            title, True, WHITE)
        if pos == 'center':
            rect = text.get_rect(center=(x, y))
        elif pos == 'topleft':
            rect = text.get_rect(topleft=(x, y))
        elif pos == 'topright':
            rect = text.get_rect(topright=(x, y))
        elif pos == 'bottomleft':
            rect = text.get_rect(bottomleft=(x, y))
        else:
            rect = text.get_rect(bottomright=(x, y))
        if obj_id is None:
            super().__init__(text=title, relative_rect=rect, manager=manager)
        else:
            super().__init__(text=title, relative_rect=rect, manager=manager,
                             object_id=obj_id)


class Button(pygame_gui.elements.UIButton):
    """Класс для кнопки"""
    def __init__(self, title, x, y, d, manager):
        """Инициализация. Принимает текст на кнопке, положение, изменение
        размера кнопки и менеджер"""
        text = MAIN_FONT.render(title, True, WHITE)
        rect = get_bigger_rect(
            text.get_rect(center=(x, y)), d)
        self.title = title
        self.d = d
        super().__init__(relative_rect=rect, text=title, manager=manager)

    def get_same(self, manager, x=None, y=None):
        """Функция для получения идентичной кнопки"""
        if x is None and y is None:
            return Button(self.title, self.rect.centerx, self.rect.centery,
                          self.d, manager)
        return Button(self.title, x, y, self.d, manager)


# Создание менеджеров
menu_manager = pygame_gui.UIManager((WIDTH, HEIGHT),
                                    'data/system/settings.json')
gameover_manager = pygame_gui.UIManager((WIDTH, HEIGHT),
                                        'data/system/settings.json')
game_manager = pygame_gui.UIManager((WIDTH, HEIGHT),
                                    'data/system/settings.json')
settings_manager = pygame_gui.UIManager((WIDTH, HEIGHT),
                                        'data/system/settings.json')

# Создание элементов интерфейса
QUIT_BUTTON_1 = Button('QUIT TO DESKTOP', WIDTH // 2, int(0.75 * HEIGHT), 20,
                       menu_manager)
SETTINGS_BUTTON = Button('SETTINGS', WIDTH // 2, int(0.625 * HEIGHT), 20,
                         menu_manager)
NEW_GAME_BUTTON = Button('NEW CAMPAIGN', WIDTH // 2, int(0.375 * HEIGHT), 20,
                         menu_manager)
LOAD_SAVE_BUTTON = Button('LOAD SAVE', WIDTH // 2, HEIGHT // 2, 20,
                          menu_manager)
MAIN_MENU_BUTTON = Button('MAIN MENU', WIDTH // 2, int(0.625 * HEIGHT), 20,
                          gameover_manager)
QUIT_BUTTON_2 = QUIT_BUTTON_1.get_same(gameover_manager)
RESUME_BUTTON = Button('RESUME', WIDTH // 2, int(0.250 * HEIGHT), 20,
                       game_manager)
MAIN_MENU_BUTTON_2 = MAIN_MENU_BUTTON.get_same(game_manager, WIDTH // 2,
                                               int(0.375 * HEIGHT))
LOAD_SAVE_BUTTON_2 = LOAD_SAVE_BUTTON.get_same(game_manager)
SETTINGS_BUTTON_2 = SETTINGS_BUTTON.get_same(game_manager)
QUIT_BUTTON_3 = QUIT_BUTTON_1.get_same(game_manager)
SETTINGS_LABEL = Label(36, 'SETTINGS', WIDTH // 2, HEIGHT // 8,
                       settings_manager, 'settings', 'center')
RESOLUTION_LABEL = Label(24, 'RESOLUTION', WIDTH // 5, int(0.5 * HEIGHT),
                         settings_manager, 'option', 'topleft')
VOLUME_LABEL = Label(24, 'VOLUME', WIDTH // 5, int(0.2 * HEIGHT),
                     settings_manager, 'option', 'topleft')
MUSIC_LABEL = Label(24, 'MUSIC', WIDTH // 5, int(0.3 * HEIGHT),
                    settings_manager, 'option', 'topleft')
EFFECTS_LABEL = Label(24, 'EFFECTS', WIDTH // 5, int(0.37 * HEIGHT),
                      settings_manager, 'option', 'topleft')
OK_BUTTON = Button('OK', WIDTH // 2, int(0.9 * HEIGHT), 10, settings_manager)


max_scr = max(WINDOW_SIZE, key=lambda x: len(f'{x[0]}{x[1]}'))
max_scr_text = MAIN_FONT.render(f'{max_scr[0]}X{max_scr[1]}', True, WHITE)
max_scr_rect = get_bigger_rect(max_scr_text.get_rect(
    topleft=(WIDTH // 5 + 15, int(0.6 * HEIGHT))), 15)
variantss = [f'{i[0]}X{i[1]}' for i in WINDOW_SIZE]
DROP_DOWN_MENU = pygame_gui.elements.UIDropDownMenu(
    relative_rect=max_scr_rect,
    manager=settings_manager,
    options_list=variantss,
    starting_option=variantss[0]
)

music_bar_rect = pygame.Rect(MUSIC_LABEL.rect.topright[0] + 40,
                             MUSIC_LABEL.rect.topright[1], WIDTH // 6,
                             MUSIC_LABEL.rect.height)
MUSIC_BAR = pygame_gui.elements.UIHorizontalSlider(
    manager=settings_manager,
    value_range=(0, 100),
    start_value=50,
    relative_rect=music_bar_rect
)

effect_bar_rect = pygame.Rect(EFFECTS_LABEL.rect.topright[0] + 40,
                              EFFECTS_LABEL.rect.topright[1], WIDTH // 6,
                              EFFECTS_LABEL.rect.height)
EFFECT_BAR = pygame_gui.elements.UIHorizontalSlider(
    manager=settings_manager,
    value_range=(0, 100),
    start_value=100,
    relative_rect=effect_bar_rect
)


# Создание групп с элементами
MENU_ELEMENTS = {"QUIT": QUIT_BUTTON_1, "NEW_GAME": NEW_GAME_BUTTON,
                 "LOAD": LOAD_SAVE_BUTTON, "SETTINGS": SETTINGS_BUTTON}
GAMEOVER_ELEMENTS = {"QUIT": QUIT_BUTTON_2, "MENU": MAIN_MENU_BUTTON}
IN_GAME_ELEMENTS = {"RESUME": RESUME_BUTTON, "MENU": MAIN_MENU_BUTTON_2,
                    "LOAD": LOAD_SAVE_BUTTON_2, "SETTINGS": SETTINGS_BUTTON_2,
                    "QUIT": QUIT_BUTTON_3}
SETTINGS_ELEMENTS = {"OK": OK_BUTTON, "RESOLUTION": DROP_DOWN_MENU,
                     "MUSIC": MUSIC_BAR, "EFFECTS": EFFECT_BAR}


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


class BasesLost(pygame.sprite.Sprite):
    """Класс с надписью о том, что все базы захвачены противником"""
    def __init__(self, group):
        super().__init__(group)
        txt = MAIN_FONT.render("GAME OVER. YOU'VE LOST ALL BASES", True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, int(0.375 * HEIGHT)
