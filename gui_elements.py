from Settings import WHITE, MAIN_FONT, WINDOW_SIZE, get_user_data, \
    get_bigger_rect, ICONS_GROUP, PLANE_ICON, \
    MISSILE_ICON, OIL_ICON, GEAR_ICON, RESOURCES_BASE
import pygame
import pygame_gui
import Settings

"""Создание элементов интерфейса"""


class OptionList(pygame_gui.elements.UISelectionList):
    """Класс списка позиций"""
    def __init__(self, pos1, pos2, manager):
        """Инициализация. Принимает отношение относительно ширины и высоты,
        менеджера"""
        self.pos = pos1, pos2
        self.manager = manager
        rect = MAIN_FONT.render('LOAD_SYSTEM', True, WHITE).get_rect(
            topleft=(Settings.WIDTH * pos1, Settings.HEIGHT * pos2))
        rect.width = Settings.WIDTH * 0.5
        rect.height = Settings.HEIGHT * 0.5
        data = get_user_data()
        data = ['    '.join([i, str(data[i][0])]) for i in data]
        super().__init__(relative_rect=rect, manager=manager,
                         item_list=data, object_id='saves')

    def get_same(self, manager=None):
        """Функция для получения идентичного списка"""
        manager = self.manager if manager is None else manager
        return OptionList(self.pos[0], self.pos[1], manager)


class HorizontalSlider(pygame_gui.elements.UIHorizontalSlider):
    """Класс горизонтального ползунка"""
    def __init__(self, default, rect, pos_w, d, manager,
                 relative_to_label):
        if relative_to_label == 'right':
            slider_rect = pygame.Rect(rect.topright[0] + d,
                                      rect.topright[1], Settings.WIDTH * pos_w,
                                      rect.height)
        else:
            slider_rect = pygame.Rect(rect.topleft[0] - d,
                                      rect.topleft[1], Settings.WIDTH * pos_w,
                                      rect.height)
        super().__init__(value_range=(0, 100), start_value=default,
                         manager=manager, relative_rect=slider_rect)
        self.default = default
        self.pos_w = pos_w
        self.d = d
        self.relative_to_label = relative_to_label
        self.label_rect = rect
        self.manager = manager

    def get_same(self, rect=None):
        """Функция для получения идентичного ползунка"""
        rect = self.label_rect if rect is None else rect
        return HorizontalSlider(self.get_current_value(), rect, self.pos_w,
                                self.d, self.manager, self.relative_to_label)


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

    def update_element(self):
        """"Функция для обновления выпадающего меню"""
        self.set_relative_position((Settings.WIDTH * self.pos[0],
                                   Settings.HEIGHT * self.pos[1]))


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

    def update_element(self):
        """Функция для обновления положения метки"""
        rect = self.rect
        pos = Settings.WIDTH * self.pos[0], Settings.HEIGHT * self.pos[1]
        if self.place == 'center':
            rect.center = pos
        elif self.place == 'topleft':
            rect.topleft = pos
        elif self.place == 'topright':
            rect.topright = pos
        elif self.place == 'bottomleft':
            rect.bottomleft = pos
        else:
            rect.bottomright = pos
        self.set_relative_position(rect.topleft)

    def update_text(self, txt):
        """Функция для утсановки нового текста"""
        self.set_text(str(txt))


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

    def update_element(self, pos=None):
        """Функция для обновления положения кнопки"""
        rect = self.rect
        pos1, pos2 = self.pos[0], self.pos[1] if pos is None else pos
        rect.center = Settings.WIDTH * pos1, Settings.HEIGHT * pos2
        self.set_relative_position(rect.topleft)

    def get_same(self, manager=None, pos1=None, pos2=None):
        """Функция для получения идентичной кнопки"""
        manager = self.manager if manager is None else manager
        pos1 = self.pos[0] if pos1 is None else pos1
        pos2 = self.pos[1] if pos2 is None else pos2
        return Button(self.title, pos1, pos2, self.d, manager, self.obj_id)


class Icon(pygame.sprite.Sprite):
    """Класс для иконок ресурсов"""
    def __init__(self, image, pos, group):
        """Инициализация. Принимает изрбражениеи его положение на экране"""
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center=(
            Settings.WIDTH * pos[0], Settings.HEIGHT * pos[1]))
        self.pos = pos

    def update(self):
        """Функция обновления положения иконки"""
        self.rect.center = (Settings.WIDTH * self.pos[0],
                            Settings.HEIGHT * self.pos[1])


class IconText(pygame_gui.elements.UILabel):
    """Класс для подписи к иконке"""
    def __init__(self, icon, txt, manager):
        """Инициализация. Принимает иконку, рядом с котрой должна быть
        подпись и текст"""
        self.pos = Settings.WIDTH / (icon.rect.topright[0] + 10), \
                   Settings.HEIGHT / (icon.rect.topright[1] + 15)
        txt = f'{txt}  ' if icon != OIL else f'{txt}/100'
        text = pygame.font.Font('data/font/Teletactile.ttf', 18).render(
            str(txt), True, WHITE)
        rect = text.get_rect(topleft=(icon.rect.topright[0] + 10,
                                      icon.rect.topright[1] + 12))
        self.ico = icon
        super().__init__(manager=manager, relative_rect=rect,
                         text=str(txt), object_id='caption')

    def update_element(self):
        """Функция для обновления положения подписи"""
        self.set_relative_position((Settings.WIDTH * self.pos[0],
                                    Settings.HEIGHT * self.pos[1]))

    def update_text(self):
        """Функция для обновления текста подписи"""
        text = Settings.NUM_OF_AIRCRAFT if self.ico == AIRCRAFT else \
            Settings.NUM_OF_MISSILES if self.ico == MISSILES else \
            f'{Settings.OIL_VOLUME}/100'
        self.set_text(str(text))


# Создание менеджеров
menu_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
gameover_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
game_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
settings_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
load_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
save_name_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
user_data_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
bars_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
campaign_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')
resource_manager = pygame_gui.UIManager(
    (max(Settings.WIDTH, 1920), max(Settings.HEIGHT, 1080)),
    'data/system/settings.json')


# Создание элементов интерфейса
TITLE = Label(36, 'CARRIER OPERATIONS', 0.5, 0.2, menu_manager, 'settings')
QUIT_BUTTON_1 = Button('QUIT TO DESKTOP', 0.5, 0.75, 20, menu_manager)
SETTINGS_BUTTON = Button('SETTINGS', 0.5, 0.625, 20, menu_manager)
NEW_GAME_BUTTON = Button('NEW CAMPAIGN', 0.5, 0.375, 20, menu_manager)
LOAD_SAVE_BUTTON = Button('LOAD SAVE', 0.5, 0.5, 20, menu_manager)
BASES_LOST = Label(36, "GAME OVER. YOU'VE LOST ALL THE BASES", 0.5, 0.375,
                   gameover_manager, 'settings')
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
MUSIC_BAR = HorizontalSlider(20, MUSIC_LABEL.rect, 0.16, 40,
                             bars_manager, 'right')
EFFECT_BAR = HorizontalSlider(100, EFFECTS_LABEL.rect, 0.16, 30,
                              bars_manager, 'right')
FULLSCREEN_LABEL = Label(24, 'FULLSCREEN', 0.6, 0.2,
                         settings_manager, 'option', 'topleft')
FULLSCREEN_BUTTON = Button(' ', 0.66, 0.27, 5, settings_manager,
                           'stable_btn')
LOAD_LABEL = Label(36, 'SAVE AND LOAD', 0.5, 0.1, load_manager, 'settings',
                   'center')
TO_SAVE_BUTTON = Button('SAVE', 0.7, 0.35, 15, load_manager, 'stable_btn')
TO_LOAD_BUTTON = Button('LOAD', 0.7, 0.45, 15, load_manager, 'stable_btn')
TO_DELETE_BUTTON = Button('DELETE', 0.7, 0.55, 15, load_manager, 'stable_btn')
USERS_LIST = OptionList(0.1, 0.25, user_data_manager)
OK_BUTTON_LOAD = Button('OK', 0.5, 0.9, 10, load_manager)
RESOURCES_LABEL = Label(36, 'RESOURCES ON THE MAIN BASE', 0.5, 0.1,
                        resource_manager, 'settings', 'center')
AIRCRAFT = Icon(PLANE_ICON, (0.20, 0.04), ICONS_GROUP)
MISSILES = Icon(MISSILE_ICON, (0.27, 0.04), ICONS_GROUP)
OIL = Icon(OIL_ICON, (0.34, 0.04), ICONS_GROUP)
AIRCRAFT_CAPTION = IconText(AIRCRAFT, Settings.NUM_OF_AIRCRAFT,
                            campaign_manager)
MISSILES_CAPTION = IconText(MISSILES, Settings.NUM_OF_MISSILES,
                            campaign_manager)
OIL_CAPTION = IconText(OIL, Settings.OIL_VOLUME, campaign_manager)
AIRCRAFT_BASE = Icon(PLANE_ICON, (0.12, 0.2), RESOURCES_BASE)
MISSILES_BASE = Icon(MISSILE_ICON, (0.12, 0.4), RESOURCES_BASE)
GEARS_BASE = Icon(GEAR_ICON, (0.12, 0.8), RESOURCES_BASE)
OIL_BASE = Icon(OIL_ICON, (0.12, 0.6), RESOURCES_BASE)
AIRCRAFT_BASE_CAPT = Label(24, 'AIRCRAFT', 0.3, 0.2,
                           resource_manager, 'option', 'center')
MISSILES_BASE_CAPT = Label(24, 'MISSILES', 0.3, 0.4,
                           resource_manager, 'option', 'center')
GEARS_BASE_CAPT = Label(24, 'REPAIR PARTS', 0.3, 0.8,
                        resource_manager, 'option', 'center')
OIL_BASE_CAPT = Label(24, 'OIL VOLUME', 0.3, 0.6,
                      resource_manager, 'option', 'center')
AIR_NUM = Label(24, f'  {Settings.BASE_NUM_OF_AIRCRAFT}', 0.5, 0.2,
                resource_manager, 'option', 'center')
MIS_NUM = Label(24, f'  {Settings.BASE_NUM_OF_MISSILES}', 0.5, 0.4,
                resource_manager, 'option', 'center')
OIL_NUM = Label(24, f'  {Settings.BASE_OIL_VOLUME}', 0.5, 0.6,
                resource_manager, 'option', 'center')
REP_NUM = Label(24, f'  {Settings.BASE_NUM_OF_REPAIR_PARTS}', 0.5, 0.8,
                resource_manager, 'option', 'center')
CAPTIONS = [AIRCRAFT_CAPTION, MISSILES_CAPTION, OIL_CAPTION]
# Создание групп с элементами
LABELS = [TITLE, BASES_LOST, RESOLUTION_LABEL, SETTINGS_LABEL, VOLUME_LABEL,
          EFFECTS_LABEL, MUSIC_LABEL, FULLSCREEN_LABEL, LOAD_LABEL,
          RESOURCES_LABEL, AIRCRAFT_BASE_CAPT, MISSILES_BASE_CAPT,
          GEARS_BASE_CAPT, OIL_BASE_CAPT, AIR_NUM, MIS_NUM, OIL_NUM, REP_NUM]
MENU_ELEMENTS = {"QUIT": QUIT_BUTTON_1, "NEW_GAME": NEW_GAME_BUTTON,
                 "LOAD": LOAD_SAVE_BUTTON, "SETTINGS": SETTINGS_BUTTON}
GAMEOVER_ELEMENTS = {"QUIT": QUIT_BUTTON_2, "MENU": MAIN_MENU_BUTTON}
IN_GAME_ELEMENTS = {"QUIT": QUIT_BUTTON_3, "RESUME": RESUME_BUTTON,
                    "MENU": MAIN_MENU_BUTTON_2, "LOAD": LOAD_SAVE_BUTTON_2,
                    "SETTINGS": SETTINGS_BUTTON_2}
SETTINGS_ELEMENTS = {"OK": OK_BUTTON, "RESOLUTION": DROP_DOWN_MENU,
                     "MUSIC": MUSIC_BAR, "EFFECTS": EFFECT_BAR,
                     'FULLSCREEN': FULLSCREEN_BUTTON}
LOAD_ELEMENTS = {'TO_SAVE': TO_SAVE_BUTTON, 'TO_LOAD': TO_LOAD_BUTTON,
                 'LIST': USERS_LIST, 'TO_DELETE': TO_DELETE_BUTTON,
                 'OK': OK_BUTTON_LOAD}