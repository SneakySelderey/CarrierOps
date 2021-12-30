import pygame
import pygame_gui
import sys
import random
from math import hypot
from board import Board
from player import Player
from AI import AI
from base import Base
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
    [i.stop() for i in ALL_SOUNDS]
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
    global WIDTH, HEIGHT, help_surface, screen
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
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == SETTINGS_ELEMENTS['RESOLUTION']:
                        # Изменение размера окна
                        WIDTH, HEIGHT = map(int, event.text.split('X'))
                        Settings.WIDTH, Settings.HEIGHT = WIDTH, HEIGHT
                        Settings.CELL_SIZE = WIDTH // 25
                        gui_elements.WIDTH, gui_elements.HEIGHT = WIDTH, HEIGHT
                        pygame.display.set_mode((WIDTH, HEIGHT))
                        rebase_elements()
                        help_surface = pygame.transform.scale(help_surface,
                                                              (WIDTH, HEIGHT))
                        background = pygame.transform.scale(
                            SETTINGS_BACKGROUND, (WIDTH, HEIGHT))
                        #background2 = pygame.transform.scale(background2,
                        #                                     (WIDTH, HEIGHT))
                        game_objects.all_sprites.update()
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Изменение громкости звуков или музыки
                    if event.ui_element == SETTINGS_ELEMENTS['EFFECTS']:
                        [i.set_volume(event.value / 10) for i in ALL_SOUNDS]
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
    background = pygame.transform.scale(GAMEOVER_SCREEN, (WIDTH, HEIGHT))
    alpha = 255
    screen.fill(BLACK)
    gameover_group.draw(screen)
    pygame.display.flip()
    sleep(1)
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
            game_manager.process_events(event)
        game_manager.update(delta)
        screen.blit(help_surface_2, (0, 0))
        help_surface.fill((0, 0, 0, alpha))
        screen.blit(help_surface, (0, 0))
        game_manager.draw_ui(screen)
        pygame.display.flip()
        alpha = min(alpha + 20, 200)
        clock.tick(FPS)


class Run:
    """Класс, в котором обрабатываются все основные игровые события"""
    def __init__(self):
        self.cell_size = CELL_SIZE
        self.cells_x = WIDTH // self.cell_size
        self.cells_y = HEIGHT // self.cell_size

        self.board = Board(self.cells_x, self.cells_y, self.cell_size)
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
        self.game_sprites = pygame.sprite.Group()

        self.player = Player(True)
        self.destination_player = self.player.rect.center
        self.ai = AI(False)
        self.bases = []
        for i in range(10):
            x = random.randint(0, self.cells_x - 1) * self.cell_size
            y = random.randint(0, self.cells_y - 1) * self.cell_size
            self.bases.append(Base(x, y, 'neutral', True, self.cell_size))
        self.friendly_missiles = []
        self.hostile_missiles = []
        self.friendly_aircraft = []
        self.list_all_sprites = [self.player, self.ai, self.bases,
                                 self.friendly_missiles,
                                 self.hostile_missiles, self.friendly_aircraft]

    def missile_launch(self, destination):
        """Функция для запуска противокорабельной ракеты"""
        self.friendly_missiles.append(MissileFriendly(
            self.player, destination, self.ai, True))
        FIRE_VLS.play()

    def aircraft_launch(self, destination):
        self.friendly_aircraft.append(AircraftFriendly(
            self.player, destination, self.ai, True))
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
                screen, BLUE, (destination[0], destination[1]), 10)
        return [stop_x, stop_y]

    def destination_ai(self):
        """Расчет точки движания для ИИ"""
        distance = []
        ai_pos_x = self.ai.rect.centerx // self.cell_size
        ai_pos_y = self.ai.rect.centery // self.cell_size
        for i in self.bases:
            base_x = i.rect.centerx // self.cell_size
            base_y = i.rect.centery // self.cell_size
            dist = [ai_pos_x - base_x, ai_pos_y - base_y]
            if [base_x, base_y] not in self.hostile_bases:
                distance.append(
                    (dist, [i.rect.centerx, i.rect.centery]))
        try:
            destination_ai = min(distance)
            idx = distance.index(destination_ai)
            dest = self.move(distance[idx][1], self.ai)
            self.base_lost(dest, distance[idx][1])
        except ValueError:
            self.defeat = True
            [sound.stop() for sound in ALL_SOUNDS]

    def base_taken(self, dest, destination):
        """Функия дял захвата базы союзником"""
        if dest[0] and dest[1]:
            player_grid_x = destination[0] // self.cell_size
            player_grid_y = destination[1] // self.cell_size
            for i in self.bases:
                base_x = i.rect.centerx // self.cell_size
                base_y = i.rect.centery // self.cell_size
                if base_x == player_grid_x and base_y == player_grid_y:
                    i.update('friendly')
                    if [base_x, base_y] in self.hostile_bases:
                        self.hostile_bases.remove([base_x, base_y])

    def base_lost(self, dest, destination):
        """Функция для захвата базы противником"""
        if dest[0] and dest[1]:
            ai_grid_x = destination[0] // self.cell_size
            ai_grid_y = destination[1] // self.cell_size
            for i in self.bases:
                base_x = i.rect.centerx // self.cell_size
                base_y = i.rect.centery // self.cell_size
                if base_x == ai_grid_x and base_y == ai_grid_y:
                    i.update('hostile')
                    self.hostile_bases.append([base_x, base_y])

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
            if hypot(missile_x - ai_x, missile_y - ai_y) <= 150:
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
                               150, 1)

        # если противник обнаружен самолетом
        air_tracking = False
        for aircraft in self.friendly_aircraft:
            air_x, air_y = aircraft.rect.center
            # если цель в радиусе обнаружения самолета, то
            # поднимается соответствующий флаг
            if hypot(air_x - ai_x, air_y - ai_y) <= 250:
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
                               250, 1)

        # отрисовка спрайта противника
        dist_between_ai_player = hypot(ai_x - player_x, ai_y - player_y)
        if dist_between_ai_player <= 300 or missile_tracking or air_tracking:
            self.ai.visibility = True
            pygame.draw.circle(screen, RED, (ai_x, ai_y), 300, 1)
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
        elif dist_between_ai_player > 300 and not missile_tracking and not air_tracking:
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
        pygame.draw.circle(screen, BLUE, (player_x, player_y), 300, 1)
        pygame.draw.circle(screen, BLUE, (player_x, player_y), 1050, 1)

    def main(self):
        """Функция с основным игровым циклом"""
        alpha = 0
        alpha_menu = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.destination_player = event.pos
                        self.game_sprites.update(event.pos)
                    if event.button == 2:
                        self.aircraft_launch(event.pos)
                    if event.button == 3:
                        self.missile_launch(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_ESCAPE:
                        self.menu = not self.menu

            screen.fill(GRAY5)
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
        SUB_SUNK.play()
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
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    help_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("CarrierOps")
    clock = pygame.time.Clock()
    FPS = 60

    title_group = pygame.sprite.Group()
    Title(title_group)

    gameover_group = pygame.sprite.Group()
    BasesLost(gameover_group)

    game_objects = Run()
    menu_run, settings_run, game_run, load_run, gameover_run = \
        True, False, False, False, False
    running = True

    # Основной мега-цикл
    while running:
        # Отрисока разных экранов
        if menu_run:  # Экран меню
            result = show_menu_screen()
            game_run = result == 1
            load_run = result == 2
            settings_run = result == 3
            menu_run = False
        elif gameover_run:  # Экран после поражения
            result = show_gameover_screen()
            gameover_run = False
            menu_run = result == 1
        elif game_run:  # Игра
            game_objects = Run()
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

