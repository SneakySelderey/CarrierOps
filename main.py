from random import choice, choices
import sys
import pygame.sprite
from board import Board
from missile import Missile
from gui_elements import *
import gui_elements
from aircraft import Aircraft
from camera import Camera
from map_solomon import Map, LandCheck
from Settings import *
import Settings
import pygame_gui
from math import hypot
from player import Player
from AI import AI
import win32gui
from collections import defaultdict, deque
from datetime import datetime
import shelve
from string import ascii_letters, digits
from base import Base, SuperBase


def check(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


def give_sprites_to_check():
    """Функция, возвращающая список групп спрайтов для проверки в методе
    fog_of_war и camera_update"""
    return [Settings.BACKGROUND_MAP, Settings.BASES_SPRITES,
            Settings.PLAYER_SPRITE, Settings.MOVE_POINT_SPRITE,
            Settings.AI_SPRITE, Settings.PLAYER_MISSILES,
            Settings.PLAYER_AIRCRAFT, Settings.AI_MISSILES,
            Settings.AI_AIRCRAFT, Settings.EXPLOSION_GROUP,
            Settings.PARTICLES_GROUP]


def set_standard_values():
    """Функция для установки значений по умолчанию"""
    Settings.BASE_NUM_OF_REPAIR_PARTS = Settings.BASE_NUM_OF_MISSILES = \
        Settings.BASE_NUM_OF_AIRCRAFT = Settings.BASE_OIL_VOLUME = 0
    Settings.NUM_OF_REPAIR_PARTS = 0
    Settings.OIL_VOLUME = 100
    Settings.NUM_OF_AIRCRAFT = 3
    Settings.NUM_OF_MISSILES = 5
    Settings.LAUNCHED_MISSILES = 0
    Settings.LAUNCHED_AIRCRAFT = 0
    Settings.PLAYER_MISSILES_HIT = 0
    Settings.BASES_CAPT_AI = 0
    Settings.BASES_CAPT_PLAYER = 0
    Settings.AI_MISSILES_HIT = 0


def move_window():
    """Функция для перемещения окна на середину экрана"""
    hwnd = win32gui.FindWindow(None, "CarrierOps")
    win32gui.MoveWindow(hwnd, (
        screensize[0] - Settings.WIDTH) // 2, (
                            screensize[1] - Settings.HEIGHT) // 2,
                        Settings.WIDTH, Settings.HEIGHT, True)


def calculate_speed(cell):
    """Функция для подсчета скорости движимых объектов после изменения
    разрешения"""
    diff = 80 / cell
    Settings.PLAYER_SPEED = Settings.SPEEDS['PLAYER'] / diff
    Settings.AIR_SPEED = Settings.SPEEDS['AIRCRAFT'] / diff
    Settings.MISSILE_SPEED = Settings.SPEEDS['MISSILE'] / diff
    Settings.AI_SPEED = Settings.SPEEDS['AI'] / diff


def update_objects():
    """Функция для обновления координат игровых объектов при изменении
    разрешения/зуме"""
    Settings.PARTICLES_GROUP.empty()
    [sprite.new_position(game_objects.board.cell_size, game_objects.board.top,
                         game_objects.board.left) for sprite in
     Settings.ALL_SPRITES_FOR_SURE]
    for base in Settings.BASES_SPRITES:
        base.rect.topleft = [base.x * Settings.CELL_SIZE + Settings.LEFT,
                             base.y * Settings.CELL_SIZE + Settings.TOP]
    camera.new_position()
    calculate_speed(Settings.CELL_SIZE)
    game_objects.cell_size = Settings.CELL_SIZE


def delete_save(save):
    """Функция для удаления сохраннения из БД"""
    save = int(save) if save.isdigit() else save
    path = get_user_data()[save][1]
    CONNECTION.execute(f'''DELETE FROM PathsOfSaves 
    WHERE Path = "{path}"''')
    CONNECTION.commit()
    hash_save = path.split('/')[-1]
    system_files_to_delete = [file for file in os.listdir(
        'data/system/saves') if hash_save in file]
    for file in system_files_to_delete:
        os.remove(f'data/system/saves/{file}')
    rebase_load_manager()


def load_save(title):
    """Функция для загрузи сохранения"""
    global chosen_map, game_objects
    title = int(title) if title.isdigit() else title
    with shelve.open(get_user_data()[title][1]) as data:
        # Загрузим ресурсы
        Settings.BOARD = data['board']
        Settings.LAUNCHED_MISSILES = data['launched_missiles']
        Settings.LAUNCHED_AIRCRAFT = data['launched_aircraft']
        Settings.PLAYER_MISSILES_HIT = data['player_hit']
        Settings.AI_MISSILES_HIT = data['ai_hit']
        Settings.BASES_CAPT_PLAYER = data['player_captured']
        Settings.BASES_CAPT_AI = data['ai_captured']
        Settings.OIL_VOLUME = data['player_oil']
        Settings.NUM_OF_AIRCRAFT = data['player_aircraft']
        Settings.NUM_OF_MISSILES = data['player_missiles']
        Settings.BASE_OIL_VOLUME = data['base_oil']
        Settings.BASE_NUM_OF_AIRCRAFT = data['base_aircraft']
        Settings.BASE_NUM_OF_MISSILES = data['base_missiles']
        Settings.BASE_NUM_OF_REPAIR_PARTS = data['base_repair_parts']
        Settings.CELL_SIZE = data['cell_size']
        Settings.TOP = data['game']['board'].top
        Settings.LEFT = data['game']['board'].left

        # Загрузим класс для игры
        chosen_map = data['map']['chosen_map']
        if game_objects is None:
            game_objects = Run()
        clear_sprite_groups()
        for i, j in data['game'].items():
            game_objects.__dict__[i] = j
        # Загрузим камеру
        for i, j in data['camera'].items():
            camera.__dict__[i] = j
        # Загузим карту
        Map(data['map']['visibility'], game_objects.board,
            data['map']['chosen_map'])
        LandCheck(game_objects.board)
        # Загрузим игрока и ИИ
        for carrier in data['carriers']:
            new_carrier = Player() if carrier['obj'] == 'player' else AI()
            for i, j in carrier.items():
                new_carrier.__dict__[i] = j
        # Загрузим самолеты
        for aircraft in data['aircraft']:
            if aircraft[0] == 'friendly':
                new_air = Aircraft(aircraft[1]['destination'],
                                   aircraft[1]['visibility'])
            else:
                pass  # TODO: HOSTILE AIRCRAFT
            for i, j in aircraft[1].items():
                new_air.__dict__[i] = j
        # Загрузим базы
        for base in data['bases']:
            if base[0] == 'base':
                new_base = Base(base[1]['x'], base[1]['y'],
                                base[1]['state'],
                                base[1]['visibility'])
            else:
                new_base = SuperBase(base[1]['x'], base[1]['y'],
                                     base[1]['state'],
                                     base[1]['visibility'])
            for i, j in base[1].items():
                new_base.__dict__[i] = j
        # Загрузим ракеты
        for missile in data['missiles']:
            new_mis = Missile(
                missile[1]['rect'].center, missile[1]['activation'],
                missile[1]['visibility'], missile[1]['obj'])
            for i, j in missile[1].items():
                new_mis.__dict__[i] = j
    update_objects()
    game_objects.menu = False
    Settings.IS_PAUSE = True
    calculate_speed(Settings.CELL_SIZE)


def create_save(title):
    """Функция для создания сохранения"""
    now = datetime.now().strftime('%H:%M %d.%m.%y')
    random_password = ''.join(choices(ascii_letters + digits, k=10))
    CONNECTION.execute(f'''INSERT INTO PathsOfSaves(Path) VALUES 
    ("data/system/saves/{random_password}")''')
    max_rows = CONNECTION.execute('SELECT MAX(ID) '
                                  'FROM PathsOfSaves').fetchone()[0]
    CONNECTION.execute(f'''INSERT INTO Saves(Title, Date, Path) VALUES(
    "{title}", "{now}", {max_rows})''')
    CONNECTION.commit()
    with shelve.open(f'data/system/saves/{random_password}', 'c') as data:
        data['launched_missiles'] = Settings.LAUNCHED_MISSILES
        data['launched_aircraft'] = Settings.LAUNCHED_AIRCRAFT
        data['player_hit'] = Settings.PLAYER_MISSILES_HIT
        data['ai_hit'] = Settings.AI_MISSILES_HIT
        data['player_captured'] = Settings.BASES_CAPT_PLAYER
        data['ai_captured'] = Settings.BASES_CAPT_AI
        data['player_oil'] = Settings.OIL_VOLUME
        data['player_aircraft'] = Settings.NUM_OF_AIRCRAFT
        data['player_missiles'] = Settings.NUM_OF_MISSILES
        data['base_oil'] = Settings.BASE_OIL_VOLUME
        data['base_aircraft'] = Settings.BASE_NUM_OF_AIRCRAFT
        data['base_missiles'] = Settings.BASE_NUM_OF_MISSILES
        data['base_repair_parts'] = Settings.BASE_NUM_OF_REPAIR_PARTS
        data['cell_size'] = Settings.CELL_SIZE
        data['game'] = game_objects.data_to_save()
        data['bases'] = [base.data_to_save() for base in
                         Settings.BASES_SPRITES]
        data['carriers'] = [carrier.data_to_save() for carrier in
                            Settings.CARRIER_GROUP]
        data['camera'] = camera.data_to_save()
        data['aircraft'] = [aircraft.data_to_save() for aircraft in set(
            Settings.PLAYER_AIRCRAFT) | set(Settings.AI_AIRCRAFT)]
        data['missiles'] = [missile.data_to_save() for missile in set(
            Settings.PLAYER_MISSILES) | set(Settings.AI_MISSILES)]
        data['map'] = list(Settings.BACKGROUND_MAP)[0].data_to_save()
        data['board'] = Settings.BOARD

    rebase_load_manager()


def give_tooltip(num):
    """Функция для создания подсказки. Принимает номер подсказки"""
    if num == 1:
        pygame_gui.elements.UITooltip(
            manager=user_data_manager,
            hover_distance=(1, 1),
            html_text="Сохранение не выбрано")
    elif num == 2:
        pygame_gui.elements.UITooltip(
            manager=user_data_manager,
            hover_distance=(1, 1),
            html_text="Вы не можете сохраниться, не начав игру")


def rebase_elements():
    """Функция для изменения всех элементов интерфейса"""
    user_data_manager.clear_and_reset()
    text_type_manager.clear_and_reset()
    bars_manager.clear_and_reset()
    [label.update_element() for label in LABELS]
    [element.update_element() for element in MENU_ELEMENTS.values()]
    [element.update_element() for element in MAP_ELEMENTS.values()]
    for i in gui_elements.SETTINGS_ELEMENTS:
        if i == 'MUSIC':
            gui_elements.SETTINGS_ELEMENTS[i] = SETTINGS_ELEMENTS[i].get_same(
                rect=LABELS[5].rect)
        elif i == 'EFFECTS':
            gui_elements.SETTINGS_ELEMENTS[i] = SETTINGS_ELEMENTS[i].get_same(
                rect=LABELS[4].rect)
        else:
            try:
                gui_elements.SETTINGS_ELEMENTS[i].update_element()
            except AttributeError:
                gui_elements.SETTINGS_ELEMENTS[i] = \
                    SETTINGS_ELEMENTS[i].get_same()
    [element.update_element() for element in IN_GAME_ELEMENTS.values()]
    [element.update_element() for element in GAMEOVER_ELEMENTS.values()]
    for i in gui_elements.LOAD_ELEMENTS:
        try:
            gui_elements.LOAD_ELEMENTS[i].update_element()
        except AttributeError:
            gui_elements.LOAD_ELEMENTS[i] = \
                gui_elements.LOAD_ELEMENTS[i].get_same()


def rebase_load_manager():
    """Функция для обновления элементов меню загрузки"""
    user_data_manager.clear_and_reset()
    text_type_manager.clear_and_reset()
    for i in gui_elements.LOAD_ELEMENTS:
        try:
            gui_elements.LOAD_ELEMENTS[i].update_element()
        except AttributeError:
            gui_elements.LOAD_ELEMENTS[i] = \
                gui_elements.LOAD_ELEMENTS[i].get_same()
    [label.update_element() for label in LABELS]


def clear_sprite_groups():
    """Функция для очистки групп спрайтов"""
    Settings.TO_DRAW.empty()
    Settings.EXPLOSION_GROUP.empty()
    Settings.ALL_SPRITES_FOR_SURE.empty()
    Settings.PLAYER_SPRITE.empty()
    Settings.CARRIER_GROUP.empty()
    Settings.AI_SPRITE.empty()
    Settings.BASES_SPRITES.empty()
    Settings.PLAYER_MISSILES.empty()
    Settings.PLAYER_AIRCRAFT.empty()
    Settings.AI_MISSILES.empty()
    Settings.AI_AIRCRAFT.empty()
    Settings.BACKGROUND_MAP.empty()
    Settings.FRIENDLY_BASES.clear()
    Settings.HOSTILE_BASES.clear()


def terminate():
    """"Функция для завершения работы программы"""
    pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


def show_menu_screen():
    """Фукнция для отрисовки основного меню и для работы с ним"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(MENU_BACKGROUND,
                                        (Settings.WIDTH, Settings.HEIGHT))
    alpha = 130
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == MENU_ELEMENTS['QUIT']:
                        terminate()
                    return list(MENU_ELEMENTS.values()).index(event.ui_element)
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/menu/' +
                                        choice(MENU_MUSIC))
                pygame.mixer.music.play(fade_ms=5000)
            menu_manager.process_events(event)
        # Красивая картинка
        help_surface.fill((10, 10, 10, alpha))
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        alpha = max(alpha - 10, 0)
        # Обновление менеджера
        menu_manager.update(delta)
        menu_manager.draw_ui(screen)
        pygame.display.flip()


def show_map_screen():
    """Фукнция для отрисовки меню выбора карты и для работы с ним"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(MENU_BACKGROUND,
                                        (Settings.WIDTH, Settings.HEIGHT))
    alpha = 130
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    return list(MAP_ELEMENTS.values()).index(event.ui_element)
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/menu/' +
                                        choice(MENU_MUSIC))
                pygame.mixer.music.play(fade_ms=5000)
            map_manager.process_events(event)
        # Красивая картинка
        help_surface.fill((10, 10, 10, alpha))
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        alpha = max(alpha - 10, 0)
        # Обновление менеджера
        map_manager.update(delta)
        map_manager.draw_ui(screen)
        pygame.display.flip()


def show_setting_screen(flag=True):
    """Функция для отрисовки и взаимодеййствия с окном настроек"""
    global help_surface, screen
    # Переменные для красивой картинки и эффекта затемнения
    alpha_up = 0
    alpha_down = 255
    background = pygame.transform.scale(SETTINGS_BACKGROUND, (
        Settings.WIDTH, Settings.HEIGHT))
    background2 = help_surface if not flag else pygame.transform.scale(
        MENU_BACKGROUND, (Settings.WIDTH, Settings.HEIGHT))
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == SETTINGS_ELEMENTS['OK']:
                        return 1
                    if event.ui_element == SETTINGS_ELEMENTS['FULLSCREEN']:
                        if event.ui_element.text == ' ':
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text('*')
                            screen = pygame.display.set_mode(
                                (Settings.WIDTH, Settings.HEIGHT),
                                pygame.FULLSCREEN)
                        else:
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text(' ')
                            screen = pygame.display.set_mode(
                                (Settings.WIDTH, Settings.HEIGHT))
                            move_window()
                        Settings.IS_FULLSCREEN = not Settings.IS_FULLSCREEN
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == SETTINGS_ELEMENTS['RESOLUTION']:
                        # Изменение размера окна
                        # Сохраним старое разрешение
                        Settings.P_WIDTH, Settings.P_HEIGHT = \
                            Settings.WIDTH, Settings.HEIGHT
                        # пределим новое разрешение и размер клетки
                        Settings.WIDTH, Settings.HEIGHT = map(
                            int, event.text.split('X'))
                        if Settings.P_HEIGHT != HEIGHT and \
                                Settings.P_WIDTH != WIDTH:
                            calculate_speed(Settings.CELL_SIZE)
                        Settings.CELL_SIZE = WIDTH // 20
                        # Обновим элементы интерфейса
                        rebase_elements()
                        help_surface = pygame.transform.scale(
                            help_surface, (Settings.WIDTH, Settings.HEIGHT))
                        background = pygame.transform.scale(
                            SETTINGS_BACKGROUND, (Settings.WIDTH,
                                                  Settings.HEIGHT))
                        if not Settings.IS_FULLSCREEN:
                            screen = pygame.display.set_mode(
                                (Settings.WIDTH, Settings.HEIGHT))
                        else:
                            screen = pygame.display.set_mode((Settings.WIDTH,
                                                              Settings.HEIGHT),
                                                             pygame.FULLSCREEN)
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text('*')
                        # Если игра уже начата, обновим координаты всех
                        # объектов
                        update_objects()
                        calculate_speed(Settings.CELL_SIZE)
                        if not Settings.IS_FULLSCREEN:
                            move_window()
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Изменение громкости звуков или музыки
                    if event.ui_element == SETTINGS_ELEMENTS['EFFECTS']:
                        [i.set_volume(event.value / 100) for i in ALL_EFFECTS]
                    if event.ui_element == SETTINGS_ELEMENTS['MUSIC']:
                        pygame.mixer.music.set_volume(event.value / 100)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/menu/' +
                                        choice(MENU_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            settings_manager.process_events(event)
            bars_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.blit(screen, (0, 0))
        if alpha_up < 255:
            background2.fill((0, 0, 0, alpha_up))
        alpha_up = min(alpha_up + 15, 255)
        if alpha_up == 255:
            alpha_down = max(alpha_down - 15, 150)
            screen.blit(background, (0, 0))
            background2.fill((0, 0, 0, alpha_down))
        screen.blit(background2, (0, 0))
        # Обновление менеджера
        settings_manager.update(delta)
        settings_manager.draw_ui(screen)
        bars_manager.update(delta)
        bars_manager.draw_ui(screen)
        pygame.display.flip()


def show_gameover_win_screen(gameover=True):
    """Функция для отрисовки и взаимодействия с экраном победы или поражения"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(GAMEOVER_SCREEN, (
        Settings.WIDTH, Settings.HEIGHT)) \
        if gameover else pygame.transform.scale(VICTORY, (
            Settings.WIDTH, Settings.HEIGHT))
    if gameover and list(Settings.PLAYER_SPRITE)[0].current_health <= 0:
        text = MAIN_FONT.render('GAME OVER. YOU DIED', True, WHITE)
    elif gameover:
        text = MAIN_FONT.render("GAME OVER. YOU'VE LOST ALL BASES", True,
                                WHITE)
    else:
        text = MAIN_FONT.render("VICTORY. YOU'VE CAPTURED ALL BASES",
                                True, WHITE)
    alpha = 255
    screen.fill(BLACK)
    gameover_manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(5000)
    gui_elements.MISSILES_LAUNCHED_LABEL_GO.update_text(
        'MISSILES LAUNCHED BY PLAYER: ' + str(Settings.LAUNCHED_MISSILES))
    gui_elements.AIRCRAFT_LAUNCHED_LABEL_GO.update_text(
        'AIRCRAFT LAUNCHED BY PLAYER: ' + str(Settings.LAUNCHED_AIRCRAFT))
    gui_elements.BASES_CAPTURED_BY_PLAYER_LABEL_GO.update_text(
        'BASES CAPTURED BY PLAYER: ' + str(Settings.BASES_CAPT_PLAYER))
    gui_elements.BASES_CAPTURED_BY_AI_LABEL_GO.update_text(
        'BASES CAPTURED BY AI: ' + str(Settings.BASES_CAPT_AI))
    gui_elements.PLAYER_MISSILES_HIT_LABEL_GO.update_text(
        'PLAYER MISSILES HIT: ' + str(Settings.PLAYER_MISSILES_HIT))
    gui_elements.AI_MISSILES_HIT_LABEL_GO.update_text(
        'AI MISSILES HIT: ' + str(Settings.AI_MISSILES_HIT))
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == GAMEOVER_ELEMENTS['QUIT']:
                        terminate()
                    if event.ui_element == GAMEOVER_ELEMENTS['MENU']:
                        return 1
            if event.type == MUSIC_END:
                if gameover:
                    pygame.mixer.music.load(os.getcwd() +
                                            '/data/music/gameover/'
                                            + choice(GAMEOVER_MUSIC))
                else:
                    pygame.mixer.music.load(os.getcwd() + '/data/music/win/'
                                            + choice(VICTORY_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            gameover_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.fill((0, 0, 0, alpha))
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        alpha = max(alpha - 0.5, 30)
        # Обновление менеджера
        gameover_manager.update(delta)
        gameover_manager.draw_ui(screen)
        screen.blit(text, text.get_rect(center=(
            0.5 * Settings.WIDTH, 0.1 * Settings.HEIGHT)))
        pygame.display.flip()


def show_in_game_menu(from_game=True):
    """Функция для отрисовки и взаимодействия с внутриигровым меню"""
    # Переменные для создания красивой картинки
    help_surface_2 = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                    pygame.SRCALPHA)
    help_surface_2.blit(game_surf, (0, 0))
    help_surface_3 = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                    pygame.SRCALPHA)

    alpha = 0 if from_game else 200
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == IN_GAME_ELEMENTS['QUIT']:
                        terminate()
                    return list(IN_GAME_ELEMENTS.values()).index(
                        event.ui_element)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/game/' +
                                        choice(GAME_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            game_manager.process_events(event)
        # Создание красивой картинки
        screen.blit(help_surface_2, (0, 0))
        help_surface_3.fill((0, 0, 0, alpha))
        screen.blit(help_surface_3, (0, 0))
        alpha = min(alpha + 20, 200)
        # Обновление менеджера
        game_manager.draw_ui(screen)
        game_manager.update(delta)
        pygame.display.flip()


def show_slides():
    """Функция для отрисовки и взаимодействия со слайдами пролога"""
    slide = pygame.transform.smoothscale(pygame.image.load(
        os.getcwd() + '/data/slides/' + next(SLIDES)), screen.get_size())
    count = -1
    pygame.mixer.music.load('data/music/spec/morse.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(os.getcwd() + '/data/music/menu/'
                                            + choice(MENU_MUSIC))
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(fade_ms=3000)
                    pygame.mixer.music.set_endevent(MUSIC_END)
                    return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        count += 1
                        slide = pygame.transform.smoothscale(pygame.image.load(
                            os.getcwd() + '/data/slides/' + next(SLIDES)),
                            screen.get_size())
                        [i.stop() for i in ALL_EFFECTS]
                        SLIDE_EFFECTS[count].play(-1)
                    except StopIteration:
                        pygame.mixer.music.load(
                            os.getcwd() + '/data/music/menu/' +
                            choice(MENU_MUSIC))
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(fade_ms=3000)
                        pygame.mixer.music.set_endevent(MUSIC_END)
                        return 1
                    except IndexError:
                        pygame.mixer.music.set_volume(0.5)
        if count == 8:
            pygame.mixer.music.fadeout(1000)
        screen.blit(slide, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def show_load_menu(from_main=True):
    """Функция для отрисовки и взаимодействия с меню сохранения и загрузки"""
    # Переменные для создания красивой картинки
    alpha_up = 0
    alpha_down = 255
    background = pygame.transform.scale(SAVE_LOAD_BACKGROUND,
                                        (Settings.WIDTH, Settings.HEIGHT))
    background2 = help_surface if not from_main else pygame.transform.scale(
        MENU_BACKGROUND, (Settings.WIDTH, Settings.HEIGHT))
    surf = pygame.Surface((int(Settings.WIDTH * 0.64),
                           int(Settings.HEIGHT * 0.4)))
    surf.set_alpha(128)
    text = MAIN_FONT.render('TYPE THE NAME OF THE SAVE', True, WHITE)
    # Переменная для выбранного элемента в списке
    item_selected = None
    to_type = False
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    create_save(event.text)
                    to_type = False
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                        not to_type:
                    if event.ui_element == LOAD_ELEMENTS['OK']:
                        return 1
                    if event.ui_element == LOAD_ELEMENTS['TO_DELETE']:
                        if item_selected is not None:
                            delete_save(item_selected)
                            item_selected = None
                        else:
                            # Если пользователь не выбрал сохранение,
                            # выведем об этом сообещние
                            give_tooltip(1)
                    if event.ui_element == LOAD_ELEMENTS['TO_LOAD']:
                        if item_selected is not None:
                            load_save(item_selected)
                            return 2 if from_main else 1
                        else:
                            # Если пользователь не выбрал сохранение,
                            # выведем об этом сообещние
                            give_tooltip(1)
                    if event.ui_element == LOAD_ELEMENTS['TO_SAVE']:
                        if not from_main:
                            to_type = True
                        else:
                            rebase_load_manager()
                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED and \
                        not to_type:
                    if event.ui_element == LOAD_ELEMENTS['TO_SAVE'] and \
                            from_main:
                        # Выведем сообщение, если пользователь решил
                        # сохраниться, не начав игру
                        give_tooltip(2)
                if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED and \
                        not to_type and event.ui_element != \
                        LOAD_ELEMENTS['LIST']:
                    rebase_load_manager()
                if event.user_type == \
                        pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and \
                        not to_type:
                    # Обновить выбранный элемент
                    item_selected = event.text.split('    ')[0]
                if event.user_type == \
                        pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION \
                        and not to_type:
                    # Загрузка сохранения
                    load_save(event.text.split('    ')[0])
                    return 2 if from_main else 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not to_type:
                        return 1
                    else:
                        to_type = False
                        rebase_load_manager()
            load_manager.process_events(event)
            user_data_manager.process_events(event)
            text_type_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.blit(screen, (0, 0))
        if alpha_up < 255:
            background2.fill((0, 0, 0, alpha_up))
        alpha_up = min(alpha_up + 15, 255)
        if alpha_up == 255:
            alpha_down = max(alpha_down - 15, 150)
            screen.blit(background, (0, 0))
            background2.fill((0, 0, 0, alpha_down))
        screen.blit(background2, (0, 0))

        # Обновление менеджера
        load_manager.update(delta)
        load_manager.draw_ui(screen)
        user_data_manager.update(delta)
        user_data_manager.draw_ui(screen)
        text_type_manager.update(delta)

        if to_type:
            screen.blit(surf, (Settings.WIDTH * 0.18,
                               Settings.HEIGHT * 0.3))
            screen.blit(text, text.get_rect(center=(Settings.WIDTH * 0.5,
                                                    Settings.HEIGHT * 0.4)))
            text_type_manager.draw_ui(screen)

        pygame.display.flip()


def show_resources_menu():
    """Функция для отрисовки меню ресурсов"""
    # Переменные для создания красивой картинки
    alpha_up = 0
    alpha_down = 255
    background = pygame.transform.scale(RESOURCE_BACKGROUND, (
        Settings.WIDTH, Settings.HEIGHT))
    background2 = help_surface
    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                    return 1
            resource_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.blit(screen, (0, 0))
        if alpha_up < 255:
            background2.fill((0, 0, 0, alpha_up))
        alpha_up = min(alpha_up + 15, 255)
        if alpha_up == 255:
            alpha_down = max(alpha_down - 15, 150)
            screen.blit(background, (0, 0))
            background2.fill((0, 0, 0, alpha_down))
        screen.blit(background2, (0, 0))
        [i.update_text(j) for i, j in zip(
            [AIR_NUM, MIS_NUM, OIL_NUM, REP_NUM], [
                Settings.BASE_NUM_OF_AIRCRAFT, Settings.BASE_NUM_OF_MISSILES,
                Settings.BASE_OIL_VOLUME, Settings.BASE_NUM_OF_REPAIR_PARTS])]
        Settings.RESOURCES_BASE.update()
        Settings.RESOURCES_BASE.draw(screen)
        # Обновление менеджера
        resource_manager.update(delta)
        resource_manager.draw_ui(screen)
        pygame.display.flip()


class Run:
    """Класс, в котором обрабатываются все основные игровые события"""

    def __init__(self):
        # self.cells_x = Settings.WIDTH * 2 // Settings.CELL_SIZE
        # self.cells_y = Settings.HEIGHT * 2 // Settings.CELL_SIZE
        self.cells_x, self.cells_y = 40, 22

        self.board = Board(self.cells_x, self.cells_y, self)
        self.board.set_view(0, 0, Settings.CELL_SIZE)

        # Флаги, переменные
        self.AI_missiles_timer = 15
        self.running = True
        self.defeat = False
        self.win = False
        self.menu = False
        self.resource_menu = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False
        self.play_main_base_detection = True

        self.g = defaultdict(list)
        n, m = self.board.height, self.board.width
        for i in range(n):
            for j in range(m):
                self.g[(i, j)] = [(i + v[0], j + v[1]) for v in Settings.N if
                                  check(i + v[0], j + v[1], n, m)]

        Map(True, self.board, chosen_map)
        LandCheck(self.board)
        self.board.add_bases()
        Player()
        AI()

    def data_to_save(self):
        """Функция, возвращающая занчения дял сохранения"""
        return self.__dict__.copy()

    def bfs(self, start, g, end):
        path = []
        visited, queue = [start], deque([start])
        p = {}
        while queue:
            vertex = queue.popleft()
            if vertex == end:
                break
            for nr in g[vertex]:
                if nr not in visited and Settings.BOARD[nr[0]][nr[1]] != 'X':
                    visited.append(nr)
                    queue.append(nr)
                    p[nr] = vertex
        if end in visited:
            to = end
            while to != start:
                path.append(to)
                to = p[to]
            path.reverse()
        return path

    def missile_launch(self, destination):
        """Функция для запуска противокорабельной ракеты"""
        Settings.PLAYER_MISSILES.add(Missile(
            list(Settings.PLAYER_SPRITE)[0].rect.center, destination, True,
            'player'))
        [mis.new_position(Settings.CELL_SIZE, self.board.top, self.board.left)
         for mis in Settings.PLAYER_MISSILES]
        FIRE_VLS.play()
        Settings.LAUNCHED_MISSILES += 1

    def aircraft_launch(self, destination):
        """Функция для запуска самолета"""
        Settings.PLAYER_AIRCRAFT.add(Aircraft(
            destination, True, list(Settings.PLAYER_SPRITE)[0]))
        TAKEOFF.play()
        Settings.LAUNCHED_AIRCRAFT += 1

    def destination_ai(self):
        """Расчет точки движания для ИИ"""
        for ai in Settings.AI_SPRITE:
            distance = []
            ai_pos_x = ai.rect.centerx // Settings.CELL_SIZE
            ai_pos_y = ai.rect.centery // Settings.CELL_SIZE
            for base in Settings.BASES_SPRITES:
                dist = hypot(ai_pos_y - base.y, ai_pos_x - base.x)
                if base.start_of_capture != 2 and base.state != 'ai':
                    distance.append(
                        (dist, [base.rect.centerx, base.rect.centery]))
            try:
                destination_ai = min(distance, key=lambda x: x[0])
                idx = distance.index(destination_ai)
                path = self.bfs(((ai.rect.centery - self.board.top) // Settings.CELL_SIZE,
                                (ai.rect.centerx - self.board.left) // Settings.CELL_SIZE),
                                self.g, ((distance[idx][-1][1] - self.board.top) // Settings.CELL_SIZE,
                                         (distance[idx][-1][0] - self.board.left) // Settings.CELL_SIZE))
                path = (path[0][1], path[0][0])
                ai.new_destination((path[0] * Settings.CELL_SIZE + Settings.CELL_SIZE / 2 + self.board.left,
                                    path[1] * Settings.CELL_SIZE + Settings.CELL_SIZE / 2 + self.board.top))
            except ValueError:
                ai.new_destination(ai.pos)
            except IndexError:
                ai.new_destination(ai.pos)

    def fog_of_war(self):
        """Отрисовка тумана войны"""
        player_x, player_y = list(Settings.PLAYER_SPRITE)[0].rect.center
        player = list(Settings.PLAYER_SPRITE)[0]

        # отрисовка нужных и скрытие ненужных спрайтов
        TO_DRAW.empty()
        [TO_DRAW.add(sprite) for group in give_sprites_to_check()
         for sprite in group if sprite.visibility]
        TO_DRAW.draw(screen)

        for base in Settings.BASES_SPRITES:
            base.show_bar = False
            if base.start_of_capture in [0, 1] or \
                    pygame.sprite.collide_circle(player, base):
                base.show_bar = True
            for aircraft in Settings.PLAYER_AIRCRAFT:
                if pygame.sprite.collide_circle(aircraft, base):
                    base.show_bar = True
            for missile in Settings.PLAYER_MISSILES:
                if pygame.sprite.collide_circle(missile, base):
                    base.show_bar = True
            for missile in Settings.AI_MISSILES:
                if pygame.sprite.collide_circle_ratio(0.65)(missile, player):
                    missile.visibility = True
                    if not missile.pause_checked:
                        Settings.IS_PAUSE = True
                        missile.pause_checked = True
                        Settings.MISSILE_DETECTION.play()
                else:
                    missile.pause_checked = False
            for air in Settings.AI_AIRCRAFT:
                if pygame.sprite.collide_circle_ratio(1)(air, player):
                    air.visibility = True
                    if not air.pause_checked:
                        Settings.IS_PAUSE = True
                        air.pause_checked = True
                        Settings.MISSILE_DETECTION.play()
                else:
                    air.pause_checked = False
            if base.show_bar and base.state == 'ai':
                base.visibility = True
                if self.play_main_base_detection:
                    MAIN_BASE_DETECTION.play()
                    self.play_main_base_detection = False

        # отрисовка спрайта противника
        for ai in Settings.AI_SPRITE:

            # проверка на обнаружение ракетой
            missile_tracking = False
            for missile in Settings.PLAYER_MISSILES:
                # если цель в радиусе обнаружения ракеты, то
                # поднимается соответствующий флаг
                missile_x, missile_y = missile.rect.center
                if pygame.sprite.collide_circle_ratio(0.35)(missile, ai):
                    missile_tracking = True
                # отрисовка радиуса обнаружения ракеты
                if not missile.activated:
                    missile.activation[0] += camera.dx
                    missile.activation[1] += camera.dy
                    pygame.draw.line(screen, BLUE, (missile_x, missile_y),
                                     (missile.activation[0],
                                      missile.activation[1]))
                pygame.draw.circle(screen, BLUE,
                                   (missile_x, missile_y),
                                   Settings.CELL_SIZE * 2, 1)

            # проверка на обнаружение самолетом
            air_tracking = False
            for aircraft in Settings.PLAYER_AIRCRAFT:
                air_x, air_y = aircraft.rect.center
                # если цель в радиусе обнаружения самолета, то
                # поднимается соответствующий флаг
                if pygame.sprite.collide_circle_ratio(0.47)(aircraft, ai):
                    air_tracking = True
                # если самолет исчерпал свой ресурс, он возвращается на
                # авианосец
                if aircraft.delete:
                    aircraft.kill()
                # отрисовка радиуса обнаружения самолета
                aircraft.destination[0] += camera.dx
                aircraft.destination[1] += camera.dy
                pygame.draw.line(screen, BLUE,
                                 (air_x, air_y),
                                 (aircraft.destination[0],
                                  aircraft.destination[1]))
                pygame.draw.circle(screen, BLUE,
                                   (air_x, air_y),
                                   Settings.CELL_SIZE * 3.5, 1)

            air_tracking_AI = False
            for aircraft in Settings.AI_AIRCRAFT:
                air_x, air_y = aircraft.rect.center
                # если цель в радиусе обнаружения самолета, то
                # поднимается соответствующий флаг
                if pygame.sprite.collide_circle_ratio(0.47)(aircraft, list(Settings.PLAYER_SPRITE)[0]):
                    air_tracking_AI = True
                    pygame.draw.circle(screen, RED,
                                       (air_x, air_y),
                                       Settings.CELL_SIZE * 3.5, 1)
                    pygame.draw.line(screen, RED,
                                     (air_x, air_y),
                                     (aircraft.destination[0],
                                      aircraft.destination[1]))
                # если самолет исчерпал свой ресурс, он возвращается на
                # авианосец
                if aircraft.delete:
                    aircraft.kill()
                # отрисовка радиуса обнаружения самолета
                aircraft.destination[0] += camera.dx
                aircraft.destination[1] += camera.dy

            if pygame.sprite.collide_circle_ratio(0.5)(player, ai) or \
                    missile_tracking or air_tracking or air_tracking_AI:
                ai.visibility = True
                if self.AI_missiles_timer >= 15:
                    ai.missile_launch(player.rect.center)
                    self.AI_missiles_timer = 0
                self.AI_missiles_timer += 0.02
                pygame.draw.circle(screen, RED, ai.rect.center,
                                   Settings.CELL_SIZE * 4, 1)
                self.play_contact_lost = True
                if self.play_new_contact:
                    if missile_tracking:
                        WEAPON_ACQUIRE.play()
                    else:
                        NEW_CONTACT.play()
                    self.play_new_contact = False
                    self.play_contact_lost = True
                    Settings.IS_PAUSE = True

            # противник прячется в тумане войны
            elif not pygame.sprite.collide_circle_ratio(0.5)(player, ai) \
                    and not missile_tracking and not air_tracking:
                ai.visibility = True
                self.play_new_contact = True
                if self.play_contact_lost:
                    CONTACT_LOST.play()
                    self.play_contact_lost = False

        # радиусы обнаружения и пуска ракет
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 4, 1)
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 15, 1)

    def camera_update(self):
        # обновляем положение всех спрайтов
        for group in give_sprites_to_check():
            for sprite in group:
                if sprite in set(Settings.PLAYER_AIRCRAFT) | set(
                    Settings.AI_AIRCRAFT) | set(Settings.PLAYER_SPRITE) | set(
                        Settings.AI_SPRITE):
                    camera.apply_aircraft(sprite)
                elif sprite in set(Settings.PLAYER_MISSILES) | set(
                        Settings.AI_MISSILES):
                    camera.apply_missiles(sprite)
                else:
                    camera.apply_rect(sprite)
        self.board.top += camera.dy
        Settings.TOP += camera.dy
        self.board.left += camera.dx
        Settings.LEFT += camera.dx
        player = list(Settings.PLAYER_SPRITE)[0]
        player.destination[0] += camera.dx
        player.destination[1] += camera.dy
        for ai in Settings.AI_SPRITE:
            ai.destination[0] += camera.dx
            ai.destination[1] += camera.dy

        if not camera.centered:
            camera.overall_shift_x += camera.dx
            camera.overall_shift_y += camera.dy
        else:
            for i in (Settings.PLAYER_AIRCRAFT, Settings.PLAYER_MISSILES,
                      Settings.AI_AIRCRAFT, Settings.AI_MISSILES):
                for j in i:
                    try:
                        j.destination[0] += camera.dx
                        j.destination[1] += camera.dy
                    except AttributeError:
                        j.activation[0] += camera.dx
                        j.activation[1] += camera.dy
        camera.centered = False

    def draw_icons_and_bars(self):
        """Функция для отрисовки иконок у баз"""
        for base in Settings.BASES_SPRITES:
            # Отрисовка иконки ресурса
            if base.state not in ['player', 'ai']:
                ico = new_image_size(Base.ResourceType[base.resource_type])
                rect = ico.get_rect(bottomleft=(
                    Settings.LEFT + (base.x + 1) * Settings.CELL_SIZE,
                    Settings.TOP + base.y * Settings.CELL_SIZE))
                screen.blit(ico, rect)
            # Отрисовка полоски захвата
            if base.show_bar and base.ticks_to_capture:
                image = pygame.Surface((int(
                    Settings.CELL_SIZE - Settings.CELL_SIZE /
                    Settings.BASE_TICKS
                    * base.ticks_to_capture), 5))
                image.fill(BLUE if base.start_of_capture == 1 else RED)
                rect = image.get_rect(topleft=(base.rect.x, base.rect.y - 10))
                screen.blit(image, rect)

    def main(self):
        """Функция с основным игровым циклом"""
        alpha = 0
        arrow_pressed = False
        pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect(10, 13, 200, 30),
            manager=campaign_manager,
            sprite_to_monitor=list(PLAYER_SPRITE)[0]
        )
        pygame.time.set_timer(FUEL_CONSUMPTION, 0)
        pygame.time.set_timer(UPDATE_ALL_SPRITES, 20)
        camera.rebase()
        camera.new_position()
        calculate_speed(Settings.CELL_SIZE)
        pygame.time.set_timer(UPDATE_ANIMATED_SPRITES, 150)
        pygame.time.set_timer(UPDATE_PARTICLES, 30)
        Settings.ALL_SPRITES_FOR_SURE.update()
        while self.running:
            from_game = True if not self.menu else False
            player = list(Settings.PLAYER_SPRITE)[0]
            delta = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player.new_destination(event.pos)
                    if event.button == 2 and Settings.NUM_OF_AIRCRAFT and \
                            Settings.OIL_VOLUME:
                        self.aircraft_launch(event.pos)
                        Settings.NUM_OF_AIRCRAFT -= 1
                        Settings.OIL_VOLUME -= 1
                    if event.button == 3 and Settings.NUM_OF_MISSILES:
                        self.missile_launch(event.pos)
                        Settings.NUM_OF_MISSILES -= 1
                    if event.button == 4 and Settings.CELL_SIZE < 200:
                        Settings.CELL_SIZE = min(
                            Settings.CELL_SIZE + 2 * Settings.CELL_SIZE / 30,
                            200)
                        update_objects()
                    if event.button == 5 and Settings.CELL_SIZE > 30:
                        Settings.CELL_SIZE = max(
                            Settings.CELL_SIZE - 2 * Settings.CELL_SIZE / 30,
                            30)
                        update_objects()
                if event.type == pygame.KEYDOWN:
                    diff = Settings.CELL_SIZE // 4
                    dx, dy = camera.dx, camera.dy
                    if event.key == pygame.K_p:
                        Settings.IS_PAUSE = not Settings.IS_PAUSE
                    if event.key == pygame.K_ESCAPE:
                        self.menu = not self.menu
                    if event.key == pygame.K_r:
                        self.resource_menu = not self.resource_menu
                    if event.key == pygame.K_c:
                        camera.new_position()
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        camera.dy = dy + diff if event.key == pygame.K_UP \
                            else dy - diff
                        arrow_pressed = True
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        camera.dx = dx + diff if event.key == pygame.K_LEFT \
                            else dx - diff
                        arrow_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        camera.dy = 0
                        arrow_pressed = False
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        camera.dx = 0
                        arrow_pressed = False
                if event.type == MUSIC_END:
                    pygame.mixer.music.load(os.getcwd() + '/data/music/game/'
                                            + choice(GAME_MUSIC))
                    pygame.mixer.music.play(fade_ms=3000)
                campaign_manager.process_events(event)
                if event.type == FUEL_CONSUMPTION and not Settings.IS_PAUSE:
                    Settings.OIL_VOLUME = max(Settings.OIL_VOLUME - 1, 0)
                if event.type == UPDATE_ALL_SPRITES and not (
                    Settings.IS_PAUSE or self.menu or self.resource_menu or
                        self.defeat):
                    Settings.ALL_SPRITES_FOR_SURE.update()
                if event.type == UPDATE_ANIMATED_SPRITES and not \
                        Settings.IS_PAUSE:
                    [sprite.update_frame() for sprite in
                     Settings.ANIMATED_SPRTIES]
                if event.type == UPDATE_PARTICLES:
                    Settings.PARTICLES_GROUP.update()

            self.camera_update()

            if not arrow_pressed:
                if Settings.WIDTH - 1 > pygame.mouse.get_pos()[0] >= \
                        Settings.WIDTH - 50:
                    camera.dx = -Settings.CELL_SIZE // 4
                elif 0 < pygame.mouse.get_pos()[0] <= 50:
                    camera.dx = Settings.CELL_SIZE // 4
                elif Settings.HEIGHT - 1 > pygame.mouse.get_pos()[1] >= \
                        Settings.HEIGHT - 50:
                    camera.dy = -Settings.CELL_SIZE // 4
                elif 0 < pygame.mouse.get_pos()[1] <= 50:
                    camera.dy = Settings.CELL_SIZE // 4
                else:
                    camera.dx = 0
                    camera.dy = 0

            if not (Settings.IS_PAUSE or self.menu or self.resource_menu or
                    self.defeat):
                [mis.update() for mis in set(Settings.PLAYER_MISSILES) | set(
                    Settings.AI_MISSILES)]
            if self.resource_menu:
                show_resources_menu()
                self.resource_menu = False
            if self.menu:
                # Получим код возврата от игрового меню
                res = show_in_game_menu(from_game)
                if res == 1:  # пользователь нажал на RESUME
                    self.menu = False
                if res == 2:  # Если нажал на MAIN MENU
                    self.running = False
                    return 2
                if res == 3:  # Если нажал на LOAD SAVE
                    show_load_menu(False)
                if res == 4:  # Если нажал на SETTINGS
                    show_setting_screen(False)
            else:
                screen.fill(DEEPSKYBLUE4)

                map_to_draw = SOLOMON_WATER if chosen_map == 'solomon' else \
                    NORWEG_WATER if chosen_map == 'norweg' else CHINA_WATER
                screen.blit(pygame.transform.scale(map_to_draw, (
                        Settings.CELL_SIZE * self.board.width,
                        Settings.CELL_SIZE * self.board.height)),
                            (self.board.left, self.board.top))
                self.board.render(screen)
                self.fog_of_war()
                self.destination_ai()
                if len([i for i in Settings.BASES_SPRITES if i.state in [
                            'player', 'friendly']]) == len(
                        Settings.BASES_SPRITES):
                    self.win = True
                    [sound.stop() for sound in ALL_EFFECTS]
                if len([i for i in Settings.BASES_SPRITES if i.state in [
                    'ai', 'hostile']]) == len(
                      Settings.BASES_SPRITES):
                    self.defeat = True
                    [sound.stop() for sound in ALL_EFFECTS]
                if player.current_health <= 0:
                    self.defeat = True
                    [sound.stop() for sound in ALL_EFFECTS]
                help_surface.fill((0, 0, 0, alpha))
                screen.blit(help_surface, (0, 0))
                [capt.update_text() for capt in CAPTIONS]
                help_surface.blit(screen, (0, 0))
                Settings.ICONS_GROUP.draw(screen)
                self.draw_icons_and_bars()

                if not player.stop:
                    pygame.draw.circle(
                        screen, BLUE, (player.destination[0],
                                       player.destination[1]),
                        Settings.CELL_SIZE // 7)

                if Settings.IS_PAUSE:
                    text_pause = MAIN_FONT.render('PAUSE', True, WHITE)
                    screen.blit(text_pause, text_pause.get_rect(
                        center=(Settings.WIDTH // 2, Settings.HEIGHT // 2)))

                if alpha == 255:
                    self.running = False
                if self.defeat or self.win:
                    alpha = min(alpha + 10, 255)

                campaign_manager.update(delta)
                campaign_manager.draw_ui(screen)
                game_surf.blit(screen, (0, 0))
                pygame.display.flip()

        # После поражения или победы
        while alpha > 0:
            help_surface.fill((0, 0, 0, alpha))
            screen.blit(help_surface, (0, 0))
            alpha -= 1
            pygame.display.flip()
            clock.tick(FPS)
        if self.defeat:
            return 1
        elif self.win:
            return 3


if __name__ == '__main__':
    # Создадим pygame-оболочку
    set_standard_values()
    pygame.init()
    pygame.mixer.init()
    size = Settings.WIDTH, Settings.HEIGHT
    screen = pygame.display.set_mode(size)
    # Вспомогательная поверхность для отрисовки
    help_surface = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                  pygame.SRCALPHA)
    game_surf = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                  pygame.SRCALPHA)
    pygame.display.set_caption("CarrierOps")
    clock = pygame.time.Clock()
    FPS = 60
    chosen_map = 'solomon'

    game_objects = Run()
    calculate_speed(Settings.CELL_SIZE)
    # Флаги, отвечающие за то, в каком меню находится пользователь
    menu_run, map_choice_run, settings_run, game_run, load_run, gameover_run, \
        victory_run, slides_run = False, False, False, False, False, False, \
        False, True
    running = True
    new_game = False
    # Создадим камеру
    camera = Camera()
    # Основной мега-цикл
    while running:
        if slides_run:  # Слайды в начале игры
            result = show_slides()
            menu_run = result == 1
            slides_run = False
        # Отрисока разных экранов
        if menu_run:  # Экран меню
            set_standard_values()
            Settings.CELL_SIZE = Settings.WIDTH // 20
            Settings.IS_PAUSE = True
            new_game = False
            pygame.mixer.music.fadeout(500)
            result = show_menu_screen()
            chosen_map = None
            map_choice_run = result == 1
            load_run = result == 2
            settings_run = result == 3
            menu_run = False
        elif map_choice_run:  # Экран выбора карты
            result = show_map_screen()
            clear_sprite_groups()
            chosen_map = 'solomon' if result == 1 else 'norweg' if \
                result == 2 else 'china'
            game_objects = Run()
            game_run = result != 0
            menu_run = result == 0
            map_choice_run = False
        elif gameover_run:  # Экран после игры
            pygame.mixer.music.fadeout(500)
            result = show_gameover_win_screen()
            set_standard_values()
            gameover_run = False
            game_objects = None
            menu_run = result == 1
        elif victory_run:  # Экран после победы
            pygame.mixer.music.fadeout(500)
            result = show_gameover_win_screen(False)
            victory_run = False
            game_objects = None
            menu_run = result == 1
        elif game_run:  # Игра
            pygame.mixer.music.fadeout(500)
            if new_game:
                clear_sprite_groups()
                set_standard_values()
                game_objects = Run()
            help_surface = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                          pygame.SRCALPHA)
            update_objects()
            result = game_objects.main()
            game_run = False
            gameover_run = result == 1
            menu_run = result == 2
        elif settings_run:  # Меню настроек
            result = show_setting_screen()
            menu_run = result == 1
            settings_run = False
        elif load_run:  # Меню загрузки
            result = show_load_menu()
            menu_run = result == 1
            game_run = result == 2
            new_game = result != 2
            load_run = False
