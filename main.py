from random import choice
import sys
import random
import pygame.sprite
from board import Board
from player import Player
from AI import AI
from friendly_missile import MissileFriendly
from gui_elements import *
from aircraft import AircraftFriendly
from camera import Camera
from map_solomon import SolomonLand, LandCheck
from Settings import *
import Settings


def delete_save(save):
    """Функция для удаления сохраннения из БД"""
    CONNECTION.execute(f'''DELETE FROM PathsOfSaves 
    WHERE Path = "{Settings.USER_DATA[save][1]}"''')
    CONNECTION.commit()
    rebase_load_manager()


def load_save(save):
    """Функция для загрузи сохранения"""
    # TODO: LOAD SAVE!!!


def create_save():
    """Функция для создания сохранения"""
    # TODO: CREATE SAVE


def give_tooltip(num):
    """Функция для создания подсказки. Принимает номер подсказки"""
    if num == 1:
        pygame_gui.elements.UITooltip(
            manager=load_manager,
            hover_distance=(1, 1),
            html_text="Сохранение не выбрано")
    elif num == 2:
        pygame_gui.elements.UITooltip(
            manager=load_manager,
            hover_distance=(1, 1),
            html_text="Вы не можете сохраниться, не начав игру")


def rebase_elements():
    """Функция для изменения всех элементов интерфейса"""
    global MENU_ELEMENTS, IN_GAME_ELEMENTS, SETTINGS_ELEMENTS, \
        GAMEOVER_ELEMENTS, LABELS, LOAD_ELEMENTS
    menu_manager.clear_and_reset()
    settings_manager.clear_and_reset()
    gameover_manager.clear_and_reset()
    game_manager.clear_and_reset()
    load_manager.clear_and_reset()
    LABELS = [i.get_same() for i in LABELS]
    MENU_ELEMENTS = {i: MENU_ELEMENTS[i].get_same() for i in MENU_ELEMENTS}
    for i in SETTINGS_ELEMENTS:
        if i == 'MUSIC':
            SETTINGS_ELEMENTS[i] = SETTINGS_ELEMENTS[i].get_same(
                rect=LABELS[4].rect)
        elif i == 'EFFECTS':
            SETTINGS_ELEMENTS[i] = SETTINGS_ELEMENTS[i].get_same(
                rect=LABELS[3].rect)
        else:
            SETTINGS_ELEMENTS[i] = SETTINGS_ELEMENTS[i].get_same()
    IN_GAME_ELEMENTS = {i: IN_GAME_ELEMENTS[i].get_same() for i in
                        IN_GAME_ELEMENTS}
    GAMEOVER_ELEMENTS = {i: GAMEOVER_ELEMENTS[i].get_same() for i in
                         GAMEOVER_ELEMENTS}
    LOAD_ELEMENTS = {i: LOAD_ELEMENTS[i].get_same() for i in LOAD_ELEMENTS}
    GAMEOVER_GROUP.update()
    TITLE_GROUP.update()


def rebase_load_manager():
    """Функция для обновления элементов меню загрузки"""
    global LOAD_ELEMENTS, LABELS
    load_manager.clear_and_reset()
    LOAD_ELEMENTS = {i: LOAD_ELEMENTS[i].get_same() for i in LOAD_ELEMENTS}
    LABELS = [i.get_same() for i in LABELS]


def clear_sprite_groups():
    """Функция для очистки групп спрайтов"""
    Settings.ALL_SPRITES_FOR_SURE.empty()
    Settings.ALL_SPRITES.empty()
    Settings.PLAYER_SPRITE.empty()
    Settings.AI_SPRITE.empty()
    Settings.BASES_SPRITES.empty()
    Settings.PLAYER_MISSILES.empty()
    Settings.PLAYER_AIRCRAFT.empty()
    Settings.AI_MISSILES.empty()
    Settings.AI_AIRCRAFT.empty()


def terminate():
    """"Функция для завершения работы программы"""
    pygame.quit()
    sys.exit()


def show_menu_screen():
    """Фукнция для отрисовки основного меню и для работы с ним"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(MENU_BACKGROUND, (WIDTH, HEIGHT))
    alpha = 130
    while True:
        delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == MENU_ELEMENTS['QUIT']:
                        terminate()
                    return list(MENU_ELEMENTS.values()).index(event.ui_element)
            if event.type == pygame.MOUSEBUTTONDOWN:
                TITLE_GROUP.update(event.pos)
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
        TITLE_GROUP.draw(screen)
        # Обновление менеджера
        menu_manager.update(delta)
        menu_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def show_setting_screen(flag=True):
    """Функция для отрисовки и взаимодеййствия с окном настроек"""
    global WIDTH, HEIGHT, help_surface, screen
    # Переменные для красивой картинки и эффекта затемнения
    fps = 240
    alpha_up = 0
    alpha_down = 255
    background = pygame.transform.scale(SETTINGS_BACKGROUND, (WIDTH, HEIGHT))
    background2 = screen if not flag else pygame.transform.scale(
        MENU_BACKGROUND, (WIDTH, HEIGHT))
    while True:
        delta = clock.tick(FPS) / 1000.0
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
                            screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                             pygame.FULLSCREEN)
                        else:
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text(' ')
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        Settings.IS_FULLSCREEN = not Settings.IS_FULLSCREEN
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == SETTINGS_ELEMENTS['RESOLUTION']:
                        # Изменение размера окна
                        # Сохраним старое разрешение
                        Settings.P_WIDTH, Settings.P_HEIGHT = WIDTH, HEIGHT
                        # пределим новое разрешение и размер клетки
                        WIDTH, HEIGHT = map(int, event.text.split('X'))
                        Settings.WIDTH, Settings.HEIGHT = WIDTH, HEIGHT
                        Settings.CELL_SIZE = WIDTH // 20
                        # Обновим элементы интерфейса
                        rebase_elements()
                        help_surface = pygame.transform.scale(help_surface,
                                                              (WIDTH, HEIGHT))
                        background = pygame.transform.scale(
                            SETTINGS_BACKGROUND, (WIDTH, HEIGHT))
                        if not Settings.IS_FULLSCREEN:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                             pygame.FULLSCREEN)
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text('*')
                        # Если игра уже начата, обновим координаты всех
                        # объектов
                        if game_objects is not None:
                            [i.new_position() for i in ALL_SPRITES_FOR_SURE]
                            game_objects.destination_player = new_coords(
                                *game_objects.destination_player)
                            game_objects.cell_size = Settings.CELL_SIZE
                            ALL_SPRITES.update()
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
        # Создание красивой картинки и эффекта затемнения
        help_surface.blit(screen, (0, 0))
        if alpha_up < 255:
            help_surface.fill((0, 0, 0, alpha_up))
            background2.set_alpha(255 - alpha_up)
        alpha_up = min(alpha_up + 15, 255)
        if alpha_up == 255:
            alpha_down = max(alpha_down - 15, 150)
            screen.blit(background, (0, 0))
            help_surface.fill((0, 0, 0, alpha_down))
        screen.blit(background2, (0, 0))
        screen.blit(help_surface, (0, 0))
        # Обновление менеджера
        settings_manager.update(delta)
        settings_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(fps)


def show_gameover_screen():
    """Функция для отрисовки и взаимодействия с экраном проигрыша"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(GAMEOVER_SCREEN, (WIDTH, HEIGHT))
    alpha = 255
    screen.fill(BLACK)
    GAMEOVER_GROUP.draw(screen)
    pygame.display.flip()
    clock.tick(5000)
    while True:
        delta = clock.tick(FPS) / 1000.0
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
                pygame.mixer.music.load(os.getcwd() + '/data/music/gameover/'
                                        + choice(GAMEOVER_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            gameover_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.fill((0, 0, 0, alpha))
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        alpha = max(alpha - 0.5, 0)
        GAMEOVER_GROUP.draw(screen)
        # Обновление менеджера
        gameover_manager.update(delta)
        gameover_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def show_in_game_menu():
    """Функция для отрисовки и взаимодействия с внутриигровым меню"""
    # Переменные для создания красивой картинки
    help_surface_2 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    help_surface_2.blit(screen, (0, 0))
    alpha = 0
    while True:
        delta = clock.tick(FPS) / 1000.0
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
        help_surface.fill((0, 0, 0, alpha))
        screen.blit(help_surface, (0, 0))
        alpha = min(alpha + 20, 200)
        # Обновление менеджера
        game_manager.draw_ui(screen)
        game_manager.update(delta)
        pygame.display.flip()
        clock.tick(FPS)


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
    fps = 240
    alpha_up = 0
    alpha_down = 255
    background = pygame.transform.scale(SAVE_LOAD_BACKGROUND, (WIDTH, HEIGHT))
    background2 = screen if not from_main else pygame.transform.scale(
        MENU_BACKGROUND, (WIDTH, HEIGHT))
    # Переменная для выбранного элемента в списке
    item_selected = None
    while True:
        delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == LOAD_ELEMENTS['OK']:
                        return 1
                    if event.ui_element == LOAD_ELEMENTS['TO_DELETE']:
                        if item_selected is not None:
                            delete_save(item_selected)
                        else:
                            # Если пользователь не выбрал сохранение,
                            # выведем об этом сообещние
                            give_tooltip(1)
                    if event.ui_element == LOAD_ELEMENTS['TO_LOAD']:
                        if item_selected is not None:
                            load_save(item_selected)
                        else:
                            # Если пользователь не выбрал сохранение,
                            # выведем об этом сообещние
                            give_tooltip(1)
                    if event.ui_element == LOAD_ELEMENTS['TO_SAVE']:
                        if not from_main:
                            pass  # TODO: SAVE
                        else:
                            rebase_load_manager()
                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if event.ui_element == LOAD_ELEMENTS['TO_SAVE'] and \
                            from_main:
                        # Выведем сообщение, если пользователь решил
                        # сохраниться, не начав игру
                        give_tooltip(2)
                if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    rebase_load_manager()
                if event.user_type == \
                        pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    # Обновить выбранный элемент
                    item_selected = event.text.split('    ')[0]
                if event.user_type == \
                        pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                    # Загрузка сохранения
                    load_save(event.text.split('    ')[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
            load_manager.process_events(event)
        # Создание красивой картинки и эффекта затемнения
        help_surface.blit(screen, (0, 0))
        if alpha_up < 255:
            help_surface.fill((0, 0, 0, alpha_up))
            background2.set_alpha(255 - alpha_up)
        alpha_up = min(alpha_up + 15, 255)
        if alpha_up == 255:
            alpha_down = max(alpha_down - 15, 150)
            screen.blit(background, (0, 0))
            help_surface.fill((0, 0, 0, alpha_down))
        screen.blit(background2, (0, 0))
        screen.blit(help_surface, (0, 0))
        # Обновление менеджера
        load_manager.update(delta)
        load_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(fps)


class Run:
    """Класс, в котором обрабатываются все основные игровые события"""
    def __init__(self):
        self.cell_size = Settings.CELL_SIZE
        self.cells_x = Settings.WIDTH * 2 // self.cell_size + 1
        self.cells_y = Settings.HEIGHT * 2 // self.cell_size + 1

        self.board = Board(self.cells_x, self.cells_y)
        self.board.set_view(0, 0, self.cell_size)

        # Флаги
        self.running = True
        self.ai_detected = False
        self.defeat = False
        self.menu = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False

        self.land_check = LandCheck(True)
        self.solomon_land = SolomonLand(True)
        self.player = Player(True)
        self.destination_player = list(self.player.rect.center)
        self.ai = AI(False)
        for i in range(10):
            x = random.randint(0, self.cells_x - 1)
            y = random.randint(0, self.cells_y - 1)
            self.board.add_base(x, y)
        self.friendly_missiles = []
        self.hostile_missiles = []
        self.friendly_aircraft = []
        self.list_all_sprites = [self.player, self.ai, self.board.bases,
                                 self.friendly_missiles,
                                 self.hostile_missiles, self.friendly_aircraft,
                                 self.solomon_land, self.land_check]

    def missile_launch(self, destination):
        """Функция для запуска противокорабельной ракеты"""
        self.friendly_missiles.append(MissileFriendly(
            destination, True))
        FIRE_VLS.play()

    def aircraft_launch(self, destination):
        """Функция для запуска самолета"""
        self.friendly_aircraft.append(AircraftFriendly(
            destination, True))
        TAKEOFF.play()

    def move(self, destination, game_obj, screen=None):
        """Движание игрока или ИИ"""
        dx, dy = destination
        center = game_obj.rect.center

        land = list(Settings.BACKGROUND_MAP)[1]
        self.land_check.rect.center = center
        if pygame.sprite.collide_mask(game_obj, land):
            N = [(0, -2), (0, 2), (2, 0), (-2, 0), (2, 2), (-2, -2), (-2, 2), (2, -2)]
            for i in N:
                game_obj.rect.center = game_obj.rect.center[0] + i[0], \
                                              game_obj.rect.center[1] + i[1]
                if not pygame.sprite.collide_mask(game_obj, land):
                    break

        game_obj.speedx = 1 if dx > center[0] else -1 if dx < center[0] else 0
        stop_x = game_obj.speedx == 0
        game_obj.speedy = 1 if dy > center[1] else -1 if dy < center[1] else 0
        stop_y = game_obj.speedy == 0
        if screen is not None and list(self.player.rect.center) != destination:
            pygame.draw.circle(
                screen, BLUE, (destination[0], destination[1]),
                Settings.CELL_SIZE // 7)
        return [stop_x, stop_y]

    def destination_ai(self):
        """Расчет точки движания для ИИ"""
        distance = []
        ai_pos_x = self.ai.rect.centerx // self.cell_size
        ai_pos_y = self.ai.rect.centery // self.cell_size
        for base in self.board.bases:
            dist = [ai_pos_x - base.x, ai_pos_y - base.y]
            if (base.x, base.y) not in Settings.HOSTILE_BASES:
                distance.append(
                    (dist, [base.rect.centerx, base.rect.centery]))
        try:
            destination_ai = min(distance)
            idx = distance.index(destination_ai)
            self.move(distance[idx][1], self.ai)
        except ValueError:
            self.defeat = True
            [sound.stop() for sound in ALL_EFFECTS]

    def fog_of_war(self):
        """Отрисовка тумана войны"""
        ai_x, ai_y = self.ai.rect.center
        player_x, player_y = self.player.rect.center
        # отрисовка спрайта противника
        for player in Settings.PLAYER_SPRITE:
            for ai in Settings.AI_SPRITE:

                # проверка на обнаружение ракетой
                missile_tracking = False
                for missile in self.friendly_missiles:
                    # если цель в радиусе обнаружения ракеты, то
                    # поднимается соответствующий флаг
                    missile_x, missile_y = missile.rect.center
                    # if hypot(missile_x - ai_x, missile_y - ai_y) <= Settings.CELL_SIZE * 2:
                    if pygame.sprite.collide_circle_ratio(0.35)(missile, ai):
                        missile_tracking = True
                    # если ракета исчерпала свой ресурс, она падает в море и
                    # спрайт удаляется
                    if missile.total_ticks >= 10:
                        self.friendly_missiles.remove(missile)
                        Settings.ALL_SPRITES.remove(missile)
                        Settings.ALL_SPRITES_FOR_SURE.remove(missile)
                    # отрисовка радиуса обнаружения ракеты
                    if not missile.activated:
                        missile.activation = list(missile.activation)
                        missile.activation[0] += camera.dx
                        missile.activation[1] += camera.dy
                        pygame.draw.line(screen, BLUE,
                                         (missile_x, missile_y),
                                         (missile.activation[0],
                                          missile.activation[1]))
                    pygame.draw.circle(screen, BLUE,
                                       (missile_x, missile_y),
                                       Settings.CELL_SIZE * 2, 1)

                # проверка на обнаружение самолетом
                air_tracking = False
                for aircraft in self.friendly_aircraft:
                    air_x, air_y = aircraft.rect.center
                    # если цель в радиусе обнаружения самолета, то
                    # поднимается соответствующий флаг
                    # if hypot(air_x - ai_x, air_y - ai_y) <= Settings.CELL_SIZE * 3.5:
                    if pygame.sprite.collide_circle_ratio(0.47)(aircraft, ai):
                        air_tracking = True
                    # если самолет исчерпала свой ресурс, он возвращается на авианосец
                    if aircraft.delete:
                        self.friendly_aircraft.remove(aircraft)
                        Settings.ALL_SPRITES.remove(aircraft)
                        Settings.ALL_SPRITES_FOR_SURE.remove(aircraft)
                    # отрисовка радиуса обнаружения самолета
                    aircraft.destination = list(aircraft.destination)
                    aircraft.destination[0] += camera.dx
                    aircraft.destination[1] += camera.dy
                    pygame.draw.line(screen, BLUE,
                                     (air_x, air_y),
                                     (aircraft.destination[0],
                                      aircraft.destination[1]))
                    pygame.draw.circle(screen, BLUE,
                                       (air_x, air_y),
                                       Settings.CELL_SIZE * 3.5, 1)

                # dist_between_ai_player = hypot(ai_x - player_x, ai_y - player_y)
                # if dist_between_ai_player <= Settings.CELL_SIZE * 4 or missile_tracking or air_tracking:
                if pygame.sprite.collide_circle_ratio(0.5)(player, ai) or missile_tracking or air_tracking:
                    self.ai.visibility = True
                    pygame.draw.circle(screen, RED, (ai_x, ai_y), Settings.CELL_SIZE * 4, 1)
                    self.ai_detected = True
                    self.play_contact_lost = True
                    if self.play_new_contact:
                        if missile_tracking:
                            WEAPON_ACQUIRE.play()
                        else:
                            NEW_CONTACT.play()
                        self.play_new_contact = False
                        self.play_contact_lost = True
                        Settings.IS_PAUSE = True
                        Settings.ALL_SPRITES.draw(screen)

                # противник прячется в тумане войны
                elif not pygame.sprite.collide_circle_ratio(0.5)(player, ai) and not missile_tracking and \
                        not air_tracking:
                    self.ai.visibility = False
                    self.ai_detected = False
                    self.play_new_contact = True
                    if self.play_contact_lost:
                        CONTACT_LOST.play()
                        self.play_contact_lost = False

        # отрисовка нужных и прятанье ненужных спрайтов
        for sprite in self.list_all_sprites:
            if type(sprite) == list:
                for i in sprite:
                    if i.visibility:
                        Settings.ALL_SPRITES.add(i)
                    else:
                        Settings.ALL_SPRITES.remove(i)
            else:
                if sprite.visibility:
                    Settings.ALL_SPRITES.add(sprite)
                else:
                    Settings.ALL_SPRITES.remove(sprite)

        # радиусы обнаружения и пуска ракет
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 4, 1)
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 15, 1)

    def camera_update(self):
        # обновляем положение всех спрайтов
        for sprite in self.list_all_sprites:
            if type(sprite) == list:
                for i in sprite:
                    if i in (Settings.PLAYER_AIRCRAFT or Settings.AI_AIRCRAFT):
                        camera.apply_aircraft(i)
                    elif i in (Settings.PLAYER_MISSILES or Settings.AI_MISSILES):
                        camera.apply_missiles(i)
                    else:
                        camera.apply_rect(i)
            else:
                camera.apply_rect(sprite)
        self.board.top += camera.dy
        self.board.left += camera.dx
        self.destination_player = list(self.destination_player)
        self.destination_player[0] += camera.dx
        self.destination_player[1] += camera.dy

    def main(self):
        """Функция с основным игровым циклом"""
        alpha = 0
        alpha_menu = 0
        arrow_pressed = False
        # water = pygame.transform.scale(Settings.SOLOMON_WATER, (Settings.WIDTH, Settings.HEIGHT))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.destination_player = list(event.pos)
                        land = list(Settings.BACKGROUND_MAP)[1]
                        land.mask = pygame.mask.from_surface(land.image)
                    if event.button == 2:
                        self.aircraft_launch(event.pos)
                    if event.button == 3:
                        self.missile_launch(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        Settings.IS_PAUSE = not Settings.IS_PAUSE
                    if event.key == pygame.K_ESCAPE:
                        self.menu = not self.menu
                    if event.key == pygame.K_UP:
                        camera.dy += 20
                        arrow_pressed = True
                    if event.key == pygame.K_DOWN:
                        camera.dy -= 20
                        arrow_pressed = True
                    if event.key == pygame.K_LEFT:
                        camera.dx += 20
                        arrow_pressed = True
                    if event.key == pygame.K_RIGHT:
                        camera.dx -= 20
                        arrow_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        camera.dy = 0
                        arrow_pressed = False
                    if event.key == pygame.K_DOWN:
                        camera.dy = 0
                        arrow_pressed = False
                    if event.key == pygame.K_LEFT:
                        camera.dx = 0
                        arrow_pressed = False
                    if event.key == pygame.K_RIGHT:
                        camera.dx = 0
                        arrow_pressed = False
                if event.type == MUSIC_END:
                    pygame.mixer.music.load(os.getcwd() + '/data/music/game/'
                                            + choice(GAME_MUSIC))
                    pygame.mixer.music.play(fade_ms=3000)

            self.camera_update()

            if pygame.mouse.get_pos()[0] >= Settings.WIDTH - 50 and not arrow_pressed:
                camera.dx = -20
            elif pygame.mouse.get_pos()[0] <= 50 and not arrow_pressed:
                camera.dx = 20
            elif pygame.mouse.get_pos()[1] >= Settings.HEIGHT - 50 and not arrow_pressed:
                camera.dy = -20
            elif pygame.mouse.get_pos()[1] <= 50 and not arrow_pressed:
                camera.dy = 20
            else:
                if not arrow_pressed:
                    camera.dx = 0
                    camera.dy = 0

            screen.fill(DEEPSKYBLUE4)
            self.board.update()
            self.board.render(screen)
            Settings.ALL_SPRITES.draw(screen)
            self.move(self.destination_player, self.player, screen)
            self.destination_ai()
            self.fog_of_war()
            help_surface.fill((0, 0, 0, alpha))
            help_surface.fill((0, 0, 0, alpha_menu))
            screen.blit(help_surface, (0, 0))

            if not (Settings.IS_PAUSE or self.defeat or self.menu):
                Settings.ALL_SPRITES.update()
                if not self.ai_detected:
                    self.ai.update()
            if Settings.IS_PAUSE:
                text_pause = MAIN_FONT.render('PAUSE', True, WHITE)
                screen.blit(text_pause, text_pause.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2)))
            if self.menu:
                # Получим код возврата от игрового меню
                result = show_in_game_menu()
                if result == 1:  # пользователь нажал на RESUME
                    self.menu = False
                if result == 2:  # Если нажал на MAIN MENU
                    self.running = False
                    return 2
                if result == 3:  # Если нажал на LOAD SAVE
                    show_load_menu(False)
                    alpha_menu = 200
                if result == 4:  # Если нажал на SETTINGS
                    show_setting_screen(False)
                    alpha_menu = 200
            if alpha == 255:
                self.running = False
            if self.defeat:
                alpha = min(alpha + 10, 255)
            if alpha_menu != 0:
                alpha_menu = max(alpha_menu - 20, 0)
            clock.tick(FPS)
            pygame.display.flip()

        # После поражения
        while alpha > 0:
            help_surface.fill((0, 0, 0, alpha))
            screen.blit(help_surface, (0, 0))
            alpha -= 1
            pygame.display.flip()
            clock.tick(FPS)
        return 1


if __name__ == '__main__':
    # Создадим pygame-оболочку
    pygame.init()
    pygame.mixer.init()
    size = Settings.WIDTH, Settings.HEIGHT
    screen = pygame.display.set_mode(size)
    # Вспомогательная поверхность для отрисовки
    help_surface = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                  pygame.SRCALPHA)
    pygame.display.set_caption("CarrierOps")
    clock = pygame.time.Clock()
    FPS = 60

    game_objects = None
    # Флаги, отвечающие за то, в каком меню находится пользователь
    menu_run, settings_run, game_run, load_run, gameover_run, slides_run = \
        False, False, False, False, False, True
    running = True
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
            pygame.mixer.music.fadeout(500)
            result = show_menu_screen()
            clear_sprite_groups()
            game_run = result == 1
            load_run = result == 2
            settings_run = result == 3
            menu_run = False
        elif gameover_run:  # Экран после поражения
            pygame.mixer.music.fadeout(500)
            result = show_gameover_screen()
            gameover_run = False
            game_objects = None
            menu_run = result == 1
        elif game_run:  # Игра
            pygame.mixer.music.fadeout(500)
            game_objects = Run()
            result = game_objects.main()
            game_run = False
            gameover_run = result == 1
            menu_run = result == 2
        elif settings_run:  # Меню настроек
            result = show_setting_screen()
            menu_run = result == 1
        elif load_run:  # Меню загрузки
            result = show_load_menu()
            menu_run = result == 1

