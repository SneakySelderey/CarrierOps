from Settings import WHITE, MAIN_FONT, WINDOW_SIZE, CONNECTION
import pygame
import pygame_gui
import Settings

"""Создание элементов интерфейса"""


def get_bigger_rect(rect, d):
    """Функция для получения увеличенного прямоугольника"""
    rect.x, rect.y, rect.width, rect.height = \
        rect.x - d, rect.y - d, rect.width + d * 2, rect.height + d * 2
    return rect


class OptionList(pygame_gui.elements.UISelectionList):
    """Класс списка позиций"""
    def __init__(self, pos1, pos2, manager):
        """Инициализация. Принимает отношение относительно ширины и высоты,
        менеджера"""
        self.pos = pos1, pos2
        self.manager = manager
        rect = MAIN_FONT.render('LOAD_SYSTEM', True, WHITE).get_rect(
            topleft=(Settings.WIDTH * pos1, Settings.HEIGHT * pos2))
        rect.width = Settings.WIDTH * 0.4
        rect.height = Settings.HEIGHT * 0.4
        data = list(CONNECTION.execute("""SELECT Saves.Title, Saves.Date, 
PathsOfSaves.Path FROM Saves INNER JOIN PathsOfSaves ON Saves.Path = 
PathsOfSaves.ID""").fetchall())
        data = ['    '.join([i[0], i[1]]) for i in data]
        super().__init__(relative_rect=rect, manager=manager,
                         item_list=data, object_id='saves')

    def get_same(self, manager=None):
        """Функция для получения идентичного списка"""
        manager = self.manager if manager is None else manager
        return OptionList(self.pos[0], self.pos[1], manager)


class HorizontalSlider(pygame_gui.elements.UIHorizontalSlider):
    """Класс горизонтального ползунка"""
    def __init__(self, start, end, default, rect, pos_w, d, manager,
                 relative_to_label):
        if relative_to_label == 'right':
            slider_rect = pygame.Rect(rect.topright[0] + d,
                                      rect.topright[1], Settings.WIDTH * pos_w,
                                      rect.height)
        else:
            slider_rect = pygame.Rect(rect.topleft[0] - d,
                                      rect.topleft[1], Settings.WIDTH * pos_w,
                                      rect.height)
        super().__init__(value_range=(start, end), start_value=default,
                         manager=manager, relative_rect=slider_rect)
        self.v_range = range(start, end + 1)
        self.default = default
        self.pos_w = pos_w
        self.d = d
        self.relative_to_label = relative_to_label
        self.label_rect = rect
        self.manager = manager

    def get_same(self, manager=None, rect=None):
        """Функция для получения идентичного ползунка"""
        manager = self.manager if manager is None else manager
        rect = self.label_rect if rect is None else rect
        return HorizontalSlider(self.v_range[0], self.v_range[-1],
                                self.default, rect, self.pos_w,
                                self.d, manager, self.relative_to_label)


class WindowSizesMenu(pygame_gui.elements.UIDropDownMenu):
    """Класс для выпадающего меню с возможными разрешениями экрана"""
    def __init__(self, pos1, pos2, d, manager, start=None):
        """Инициализация. Принимает положение относительно ширины и высоты,
        изменение размера прямоугольника и менеджер"""
        max_scr = max(WINDOW_SIZE, key=lambda x: len(f'{x[0]}{x[1]}'))
        max_scr_text = MAIN_FONT.render(f'{max_scr[0]}X{max_scr[1]}', True,
                                        WHITE)
        max_scr_rect = get_bigger_rect(max_scr_text.get_rect(
            topleft=(int(pos1 * Settings.WIDTH),
                     int(pos2 * Settings.HEIGHT))), d)
        variants = [f'{i[0]}X{i[1]}' for i in WINDOW_SIZE]
        self.d = d
        self.pos = pos1, pos2
        self.manager = manager
        start = variants[0] if start is None else start
        super().__init__(manager=manager, options_list=variants,
                         starting_option=start,
                         relative_rect=max_scr_rect)

    def get_same(self, manager=None):
        """Функция для полученяи идентичногго выпадающего спсика"""
        manager = self.manager if manager is None else manager
        return WindowSizesMenu(self.pos[0], self.pos[1], self.d, manager,
                               f'{Settings.WIDTH}X{Settings.HEIGHT}')


class Label(pygame_gui.elements.UILabel):
    """Класс для метки"""
    def __init__(self, font_size, title, pos1, pos2, manager, obj_id=None,
                 pos='center'):
        """Инициализация. Принимает размер шрифта, заголовок, положегние
        относительно ширины и высоты, менеджер, id, и часть прямоугольника,
        которую задают x и y"""
        text = pygame.font.Font('data/font/Teletactile.ttf', font_size).render(
            title, True, WHITE)
        x, y = int(Settings.WIDTH * pos1), int(Settings.HEIGHT * pos2)
        self.font_size = font_size
        self.title = title
        self.place = pos
        self.manager = manager
        self.pos = pos1, pos2
        self.obj_id = obj_id
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

    def get_same(self, manager=None):
        """Функция для получения идентичной метки"""
        manager = self.manager if manager is None else manager
        return Label(self.font_size, self.title, self.pos[0], self.pos[1],
                     manager, self.obj_id, self.place)


class Button(pygame_gui.elements.UIButton):
    """Класс для кнопки"""
    def __init__(self, title, pos1, pos2, d, manager, obj_id=None):
        """Инициализация. Принимает текст на кнопке, положение относительно
        ширины и высоты, изменение размера кнопки и менеджер"""
        text = MAIN_FONT.render(title, True, WHITE)
        rect = get_bigger_rect(
            text.get_rect(center=(int(pos1 * Settings.WIDTH),
                                  int(pos2 * Settings.HEIGHT))), d)
        self.title = title
        self.manager = manager
        self.pos = pos1, pos2
        self.d = d
        self.obj_id = obj_id
        if obj_id is None:
            super().__init__(relative_rect=rect, text=title, manager=manager)
        else:
            super().__init__(relative_rect=rect, text=title, manager=manager,
                             object_id=obj_id)

    def get_same(self, manager=None, pos1=None, pos2=None):
        """Функция для получения идентичной кнопки"""
        manager = self.manager if manager is None else manager
        pos1 = self.pos[0] if pos1 is None else pos1
        pos2 = self.pos[1] if pos2 is None else pos2
        return Button(self.title, pos1, pos2, self.d, manager, self.obj_id)


# Создание менеджеров
menu_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT),
                                    'data/system/settings.json')
gameover_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT),
                                        'data/system/settings.json')
game_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT),
                                    'data/system/settings.json')
settings_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT),
                                        'data/system/settings.json')
load_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT),
                                    'data/system/settings.json')

# Создание элементов интерфейса
QUIT_BUTTON_1 = Button('QUIT TO DESKTOP', 0.5, 0.75, 20, menu_manager)
SETTINGS_BUTTON = Button('SETTINGS', 0.5, 0.625, 20, menu_manager)
NEW_GAME_BUTTON = Button('NEW CAMPAIGN', 0.5, 0.375, 20, menu_manager)
LOAD_SAVE_BUTTON = Button('LOAD SAVE', 0.5, 0.5, 20, menu_manager)
MAIN_MENU_BUTTON = Button('MAIN MENU', 0.5, 0.625, 20, gameover_manager)
QUIT_BUTTON_2 = QUIT_BUTTON_1.get_same(gameover_manager)
RESUME_BUTTON = Button('RESUME', 0.5, 0.250, 20, game_manager)
MAIN_MENU_BUTTON_2 = MAIN_MENU_BUTTON.get_same(game_manager, 0.5, 0.375)
LOAD_SAVE_BUTTON_2 = LOAD_SAVE_BUTTON.get_same(game_manager)
SETTINGS_BUTTON_2 = SETTINGS_BUTTON.get_same(game_manager)
QUIT_BUTTON_3 = QUIT_BUTTON_1.get_same(game_manager)
SETTINGS_LABEL = Label(36, 'SETTINGS', 0.5, 0.125,
                       settings_manager, 'settings', 'center')
RESOLUTION_LABEL = Label(24, 'RESOLUTION', 0.6, 0.33,
                         settings_manager, 'option', 'topleft')
VOLUME_LABEL = Label(24, 'VOLUME', 0.2, 0.2,
                     settings_manager, 'option', 'topleft')
MUSIC_LABEL = Label(24, 'MUSIC', 0.2, 0.3,
                    settings_manager, 'option', 'topleft')
EFFECTS_LABEL = Label(24, 'EFFECTS', 0.2, 0.37,
                      settings_manager, 'option', 'topleft')

OK_BUTTON = Button('OK', 0.5, 0.8, 10, settings_manager)
DROP_DOWN_MENU = WindowSizesMenu(0.61, 0.43, 15, settings_manager)
MUSIC_BAR = HorizontalSlider(0, 100, 20, MUSIC_LABEL.rect, 0.16, 40,
                             settings_manager, 'right')
EFFECT_BAR = HorizontalSlider(0, 100, 100, EFFECTS_LABEL.rect, 0.16, 30,
                              settings_manager, 'right')
FULLSCREEN_LABEL = Label(24, 'FULLSCREEN', 0.6, 0.2,
                         settings_manager, 'option', 'topleft')
FULLSCREEN_BUTTON = Button(' ', 0.66, 0.27, 5, settings_manager,
                           'stable_btn')
LOAD_LABEL = Label(36, 'SAVE AND LOAD', 0.5, 0.1, load_manager, 'settings',
                   'center')
TO_SAVE_BUTTON = Button('SAVE', 0.15, 0.2, 15, load_manager, 'stable_btn')
TO_LOAD_BUTTON = Button('LOAD', 0.25, 0.2, 15, load_manager, 'stable_btn')
TO_DELETE_BUTTON = Button('DELETE', 0.35, 0.2, 15, load_manager, 'stable_btn')
USERS_LIST = OptionList(0.1, 0.3, load_manager)

# Создание групп с элементами
LABELS = [RESOLUTION_LABEL, SETTINGS_LABEL, VOLUME_LABEL, EFFECTS_LABEL,
          MUSIC_LABEL, FULLSCREEN_LABEL, LOAD_LABEL]
MENU_ELEMENTS = {"QUIT": QUIT_BUTTON_1, "NEW_GAME": NEW_GAME_BUTTON,
                 "LOAD": LOAD_SAVE_BUTTON, "SETTINGS": SETTINGS_BUTTON}
GAMEOVER_ELEMENTS = {"QUIT": QUIT_BUTTON_2, "MENU": MAIN_MENU_BUTTON}
IN_GAME_ELEMENTS = {"RESUME": RESUME_BUTTON, "MENU": MAIN_MENU_BUTTON_2,
                    "LOAD": LOAD_SAVE_BUTTON_2, "SETTINGS": SETTINGS_BUTTON_2,
                    "QUIT": QUIT_BUTTON_3}
SETTINGS_ELEMENTS = {"OK": OK_BUTTON, "RESOLUTION": DROP_DOWN_MENU,
                     "MUSIC": MUSIC_BAR, "EFFECTS": EFFECT_BAR,
                     'FULLSCREEN': FULLSCREEN_BUTTON}
LOAD_ELEMENTS = {'TO_SAVE': TO_SAVE_BUTTON, 'TO_LOAD': TO_LOAD_BUTTON,
                 'LIST': USERS_LIST, 'TO_DELETE': TO_DELETE_BUTTON}


class Title(pygame.sprite.Sprite):
    """Класс с названием игры"""
    def __init__(self, group):
        super().__init__(group)
        txt = MAIN_FONT.render('CARRIER OPERATIONS', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = \
            Settings.WIDTH // 2, Settings.HEIGHT // 5

    def update(self, pos=(-1, -1)):
        self.rect.centerx, self.rect.centery = Settings.WIDTH // 2, \
                                               Settings.HEIGHT // 5
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
        self.rect.centerx, self.rect.centery = Settings.WIDTH // 2, int(
            0.375 * Settings.HEIGHT)

    def update(self, *pos):
        self.rect.centerx, self.rect.centery = Settings.WIDTH // 2, int(
            0.375 * Settings.HEIGHT)
