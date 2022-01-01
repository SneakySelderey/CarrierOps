from random import choice
import sys
import random
from math import hypot
from board import Board
from player import Player
from AI import AI
from friendly_missile import MissileFriendly
from gui_elements import *
from aircraft import AircraftFriendly
from Settings import *
import Settings
import gui_elements
from time import sleep


def rebase_elements():
    """Функция для изменения всех элементов интерфейса"""
    global MENU_ELEMENTS, IN_GAME_ELEMENTS, SETTINGS_ELEMENTS, \
        GAMEOVER_ELEMENTS, LABELS
    menu_manager.clear_and_reset()
    settings_manager.clear_and_reset()
    gameover_manager.clear_and_reset()
    game_manager.clear_and_reset()
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
    gameover_group.update()
    title_group.update()


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
                title_group.update(event.pos)
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/menu/' +
                                        choice(MENU_MUSIC))
                pygame.mixer.music.play(fade_ms=5000)
            menu_manager.process_events(event)
        help_surface.fill((10, 10, 10, alpha))
        menu_manager.update(delta)
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        title_group.draw(screen)
        menu_manager.draw_ui(screen)
        pygame.display.flip()
        alpha = max(alpha - 10, 0)
        clock.tick(FPS)


def show_setting_screen(flag=True):
    """Функция для отрисовки и взаимодеййствия с окном настроек"""
    global WIDTH, HEIGHT, help_surface, screen, game_objects
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
                        Settings.P_WIDTH, Settings.P_HEIGHT = WIDTH, HEIGHT
                        WIDTH, HEIGHT = map(int, event.text.split('X'))
                        Settings.WIDTH, Settings.HEIGHT = WIDTH, HEIGHT
                        Settings.CELL_SIZE = WIDTH // 20
                        gui_elements.WIDTH, gui_elements.HEIGHT = WIDTH, HEIGHT
                        rebase_elements()
                        help_surface = pygame.transform.scale(help_surface,
                                                              (WIDTH, HEIGHT))
                        if not Settings.IS_FULLSCREEN:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                             pygame.FULLSCREEN)
                            SETTINGS_ELEMENTS['FULLSCREEN'].set_text('*')
                        if game_objects is not None:
                            for i in ALL_SPRITES:
                                i.new_position()
                            game_objects.destination_player = new_coords(
                                *game_objects.destination_player)
                            game_objects.cell_size = Settings.CELL_SIZE
                            ALL_SPRITES.update()
                        background = pygame.transform.scale(
                            SETTINGS_BACKGROUND, (WIDTH, HEIGHT))
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
        settings_manager.update(delta)
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
        settings_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(fps)


def show_gameover_screen():
    """Функция для отрисовки и взаимодействия с экраном проигрыша"""
    [i.stop() for i in ALL_EFFECTS]
    background = pygame.transform.scale(GAMEOVER_SCREEN, (WIDTH, HEIGHT))
    alpha = 255
    screen.fill(BLACK)
    gameover_group.draw(screen)
    pygame.display.flip()
    sleep(0.5)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                title_group.update(event.pos)
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/gameover/'
                                        + choice(GAMEOVER_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            gameover_manager.process_events(event)
        help_surface.fill((0, 0, 0, alpha))
        gameover_manager.update(delta)
        screen.blit(background, (0, 0))
        screen.blit(help_surface, (0, 0))
        gameover_group.draw(screen)
        gameover_manager.draw_ui(screen)
        pygame.display.flip()
        alpha = max(alpha - 0.5, 0)
        clock.tick(FPS)


def show_in_game_menu():
    """Функция для отрисовки и взаимодействия с внутриигровым меню"""
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
                    if event.ui_element == IN_GAME_ELEMENTS['RESUME']:
                        return 1
                    if event.ui_element == IN_GAME_ELEMENTS['MENU']:
                        return 2
                    if event.ui_element == IN_GAME_ELEMENTS['LOAD']:
                        return 3
                    if event.ui_element == IN_GAME_ELEMENTS['SETTINGS']:
                        return 4
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                title_group.update(event.pos)
            if event.type == MUSIC_END:
                pygame.mixer.music.load(os.getcwd() + '/data/music/game/' +
                                        choice(GAME_MUSIC))
                pygame.mixer.music.play(fade_ms=3000)
            game_manager.process_events(event)
        game_manager.update(delta)
        screen.blit(help_surface_2, (0, 0))
        help_surface.fill((0, 0, 0, alpha))
        screen.blit(help_surface, (0, 0))
        game_manager.draw_ui(screen)
        pygame.display.flip()
        alpha = min(alpha + 20, 200)
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
        delta = clock.tick(FPS) / 1000.0
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
                        try:
                            SLIDE_EFFECTS[count].play(-1)
                        except:
                            pygame.mixer.music.set_volume(0.5)
                    except StopIteration:
                        pygame.mixer.music.load(
                            os.getcwd() + '/data/music/menu/' +
                            choice(MENU_MUSIC))
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(fade_ms=3000)
                        pygame.mixer.music.set_endevent(MUSIC_END)
                        return 1
            game_manager.process_events(event)
        if count == 8:
            pygame.mixer.music.fadeout(1000)
        screen.blit(slide, (0, 0))
        game_manager.update(delta)
        pygame.display.flip()
        clock.tick(FPS)


class Run:
    """Класс, в котором обрабатываются все основные игровые события"""
    def __init__(self):
        self.cell_size = Settings.CELL_SIZE
        self.cells_x = Settings.WIDTH // self.cell_size
        self.cells_y = Settings.HEIGHT // self.cell_size

        self.board = Board(self.cells_x, self.cells_y)
        self.board.set_view(0, 0, self.cell_size)

        # Флаги
        self.running = True
        self.pause = True
        self.hostile_bases = []
        self.ai_detected = False
        self.defeat = False
        self.menu = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False

        self.all_sprites = pygame.sprite.Group()

        self.player = Player(True)
        self.destination_player = self.player.rect.center
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
                                 self.hostile_missiles, self.friendly_aircraft]

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
        game_obj.speedx = 1 if dx > center[0] else -1 if dx < center[0] else 0
        stop_x = game_obj.speedx == 0
        game_obj.speedy = 1 if dy > center[1] else -1 if dy < center[1] else 0
        stop_y = game_obj.speedy == 0
        if screen is not None and self.player.rect.center != destination:
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
            if [base.x, base.y] not in self.hostile_bases:
                distance.append(
                    (dist, [base.rect.centerx, base.rect.centery]))
        try:
            destination_ai = min(distance)
            idx = distance.index(destination_ai)
            dest = self.move(distance[idx][1], self.ai)
            self.base_lost(dest, distance[idx][1])
        except ValueError:
            self.defeat = True
            [sound.stop() for sound in ALL_EFFECTS]

    def base_taken(self, dest, destination):
        """Функия дял захвата базы союзником"""
        if dest[0] and dest[1]:
            player_grid_x = destination[0] // Settings.CELL_SIZE
            player_grid_y = destination[1] // Settings.CELL_SIZE
            for base in self.board.bases:
                if base.x == player_grid_x and base.y == player_grid_y:
                    base.update('friendly')
                    if [base.x, base.y] in self.hostile_bases:
                        self.hostile_bases.remove([base.x, base.y])

    def base_lost(self, dest, destination):
        """Функция для захвата базы противником"""
        if dest[0] and dest[1]:
            ai_grid_x = destination[0] // Settings.CELL_SIZE
            ai_grid_y = destination[1] // Settings.CELL_SIZE
            for base in self.board.bases:
                if base.x == ai_grid_x and base.y == ai_grid_y:
                    base.update('hostile')
                    self.hostile_bases.append([base.x, base.y])

    def fog_of_war(self):
        """Отрисовка тумана войны"""
        # если противник обнаружен ракетой
        missile_tracking = False
        ai_x, ai_y = self.ai.rect.center
        player_x, player_y = self.player.rect.center
        for missile in self.friendly_missiles:
            # если цель в радиусе обнаружения ракеты, то
            # поднимается соответствующий флаг
            missile_x, missile_y = missile.rect.center
            if hypot(missile_x - ai_x, missile_y - ai_y) <= \
                    Settings.CELL_SIZE * 2:
                missile_tracking = True
            # если ракета исчерпала свой ресурс, она падает в море и
            # спрайт удаляется
            if missile.total_ticks >= 10:
                self.friendly_missiles.remove(missile)
                self.all_sprites.remove(missile)
            # отрисовка радиуса обнаружения ракеты
            if not missile.activated:
                pygame.draw.line(screen, BLUE,
                                 (missile_x, missile_y),
                                 (missile.activation[0],
                                  missile.activation[1]))
            pygame.draw.circle(screen, BLUE,
                               (missile_x, missile_y),
                               Settings.CELL_SIZE * 2, 1)

        # если противник обнаружен самолетом
        air_tracking = False
        for aircraft in self.friendly_aircraft:
            air_x, air_y = aircraft.rect.center
            # если цель в радиусе обнаружения самолета, то
            # поднимается соответствующий флаг
            if hypot(air_x - ai_x, air_y - ai_y) <= Settings.CELL_SIZE * 3.5:
                air_tracking = True
            # если самолет исчерпала свой ресурс, он возвращается на авианосец
            if aircraft.delete:
                self.friendly_aircraft.remove(aircraft)
                self.all_sprites.remove(aircraft)
            # отрисовка радиуса обнаружения самолета
            pygame.draw.line(screen, BLUE,
                             (air_x, air_y),
                             (aircraft.destination[0],
                              aircraft.destination[1]))
            pygame.draw.circle(screen, BLUE,
                               (air_x, air_y),
                               Settings.CELL_SIZE * 3.5, 1)

        # отрисовка спрайта противника
        dist_between_ai_player = hypot(ai_x - player_x, ai_y - player_y)
        if dist_between_ai_player <= Settings.CELL_SIZE * 4 or \
                missile_tracking or air_tracking:
            self.ai.visibility = True
            pygame.draw.circle(screen, RED, (ai_x, ai_y),
                               Settings.CELL_SIZE * 4, 1)
            self.ai_detected = True
            self.play_contact_lost = True
            if self.play_new_contact:
                if missile_tracking:
                    WEAPON_ACQUIRE.play()
                else:
                    NEW_CONTACT.play()
                self.play_new_contact = False
                self.play_contact_lost = True
                self.pause = True
                self.all_sprites.draw(screen)

        # противник прячется в тумане войны
        elif dist_between_ai_player > Settings.CELL_SIZE * 4 and \
                not missile_tracking and not air_tracking:
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
                        self.all_sprites.add(i)
                    else:
                        self.all_sprites.remove(i)
            else:
                if sprite.visibility:
                    self.all_sprites.add(sprite)
                else:
                    self.all_sprites.remove(sprite)

        # радиусы обнаружения и пуска ракет
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 4, 1)
        pygame.draw.circle(screen, BLUE, (player_x, player_y),
                           Settings.CELL_SIZE * 15, 1)

    def main(self):
        """Функция с основным игровым циклом"""
        alpha = 0
        alpha_menu = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.get_cell(event.pos)
                    if event.button == 1:
                        self.destination_player = event.pos
                    if event.button == 2:
                        self.aircraft_launch(event.pos)
                    if event.button == 3:
                        self.missile_launch(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_ESCAPE:
                        self.menu = not self.menu
                if event.type == MUSIC_END:
                    pygame.mixer.music.load(os.getcwd() + '/data/music/game/'
                                            + choice(GAME_MUSIC))
                    pygame.mixer.music.play(fade_ms=3000)

            screen.fill(GRAY5)
            self.board.update()
            self.board.render(screen)
            self.all_sprites.draw(screen)
            goal = self.move(self.destination_player, self.player, screen)
            self.base_taken(goal, self.destination_player)
            self.destination_ai()
            self.fog_of_war()
            help_surface.fill((0, 0, 0, alpha))
            help_surface.fill((0, 0, 0, alpha_menu))
            screen.blit(help_surface, (0, 0))

            if not (self.pause or self.defeat or self.menu):
                self.all_sprites.update()
                if not self.ai_detected:
                    self.ai.update()
            if self.pause:
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
                    alpha_menu = 0
                    pass  # TODO: LOAD
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
    pygame.init()
    pygame.mixer.init()
    size = Settings.WIDTH, Settings.HEIGHT
    screen = pygame.display.set_mode(size)
    help_surface = pygame.Surface((Settings.WIDTH, Settings.HEIGHT),
                                  pygame.SRCALPHA)
    pygame.display.set_caption("CarrierOps")
    clock = pygame.time.Clock()
    FPS = 60

    title_group = pygame.sprite.Group()
    Title(title_group)

    gameover_group = pygame.sprite.Group()
    BasesLost(gameover_group)

    game_objects = None
    menu_run, settings_run, game_run, load_run, gameover_run, slides_run = \
        False, False, False, False, False, True
    running = True

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
            [sprite.kill() for sprite in ALL_SPRITES]
            [sprite.kill() for sprite in PLAYER_SPRITE]
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
            a = game_objects.board.board
            result = game_objects.main()
            game_run = False
            gameover_run = result == 1
            menu_run = result == 2
        elif settings_run:  # Меню настроек
            result = show_setting_screen()
            menu_run = result == 1
        elif load_run:  # Меню загрузки
            pass  # TODO: LOAD
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(BLACK)
        pygame.display.flip()

