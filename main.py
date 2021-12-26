import pygame
import random
from math import sqrt
from board import Board
from player import Player
from AI import AI
from base import Base
from friendly_missile import MissileFriendly
from Settings import *


class Run:
    """Класс, в котором обрабатываются все основные игровые события"""
    def __init__(self):
        self.cell_size = CELL_SIZE
        self.cells_x = WIDTH // self.cell_size
        self.cells_y = HEIGHT // self.cell_size

        self.board = Board(self.cells_x, self.cells_y, self)
        self.board.set_view(0, 0, self.cell_size)

        # Озвучка событий
        self.sound_new_contact = NEW_CONTACT
        self.sound_contact_lost = CONTACT_LOST
        self.sound_fire_VLS = FIRE_VLS
        self.sound_weapon_acquire = WEAPON_ACQUIRE
        self.sound_explosion = EXPLOSION

        # Флаги
        self.running = True
        self.pause = True
        self.hostile_bases = []
        self.ai_detected = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False
        self.missile = False

        self.all_sprites = pygame.sprite.Group()
        self.player = Player(True)
        self.ai = AI(False)
        self.bases = []
        for i in range(10):
            x = random.randint(0, self.cells_x - 1) * self.cell_size
            y = random.randint(0, self.cells_y - 1) * self.cell_size
            self.bases.append(Base(x, y, 'neutral', True, self.cell_size))
        self.friendly_missiles = []
        self.hostile_missiles = []
        self.list_all_sprites = [self.player, self.ai, self.bases,
                                 self.friendly_missiles, self.hostile_missiles]

    def missile_launch(self, destination):
        """Функция для запуска противокорабельной ракеты"""
        self.friendly_missiles.append(MissileFriendly(
            self.player, True, destination, self.ai, True,
            self.sound_explosion))
        self.sound_fire_VLS.play()

    def movement(self, destination, game_obj, screen=None):
        """Движание игрока или ИИ"""
        dx, dy = destination
        center = game_obj.rect.center
        game_obj.speedx = 1 if dx > center[0] else -1 if dx < center[0] else 0
        stop_x = game_obj.speedx == 0
        game_obj.speedy = 1 if dy > center[1] else -1 if dy < center[1] else 0
        stop_y = game_obj.speedy == 0
        if screen is not None:
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
            dest = self.movement(distance[idx][1], self.ai)
            self.base_lost(dest, distance[idx][1])
        except ValueError:
            self.running = False
            print('Вы проиграли!')

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

    def set_pause(self, screen, pause_screen):
        """Функиця, ставящая игру на паузу"""
        if not self.pause:
            self.all_sprites.update()
            if not self.ai_detected:
                self.ai.update()
            pygame.display.flip()
            screen.fill(GRAY5)
            self.board.render(screen)
            self.all_sprites.draw(screen)
        else:
            self.board.render(screen)
            self.all_sprites.draw(screen)
            pause_screen.blit(SC_TEXT, POS)
            pygame.display.flip()

    def fog_of_war(self, ai, player, bases, screen):
        # если противник обнаружен ракетой
        missile_tracking = False
        for missile in self.friendly_missiles:
            # если цель в радиусе обнаружения ракеты, то
            # поднимается соответствующий флаг
            if (sqrt((missile.rect.centerx - ai.rect.centerx) ** 2 + (
                missile.rect.centery - ai.rect.centery) ** 2)) \
                    <= 150:
                missile_tracking = True
            # если ракета исчерпала свой ресурс, она падает в море и
            # спрайт удаляется
            if missile.total_ticks >= 10:
                self.friendly_missiles.remove(missile)
                self.all_sprites.remove(missile)
            # отрисовка радиуса обнаружения ракеты
            if not missile.activated:
                pygame.draw.line(screen, BLUE,
                                 (missile.rect.centerx, missile.rect.centery),
                                 (missile.activation[0], missile.activation[1]))
            pygame.draw.circle(screen, BLUE,
                               (missile.rect.centerx, missile.rect.centery),
                               150, 1)

        # отрисовка спрайта противника
        if (sqrt((ai.rect.centerx - player.rect.centerx) ** 2 + (
            ai.rect.centery - player.rect.centery) ** 2)) \
                <= 300 or missile_tracking:
            ai.visibility = True
            pygame.draw.circle(screen, RED,
                               (ai.rect.centerx, ai.rect.centery), 300, 1)
            self.ai_detected = True
            self.play_contact_lost = True
            if self.play_new_contact:
                if missile_tracking:
                    self.sound_weapon_acquire.play()
                else:
                    self.sound_new_contact.play()
                self.play_new_contact = False
                self.play_contact_lost = True
                self.pause = True
                self.all_sprites.draw(screen)

        # противник прячется в тумане войны
        elif (sqrt((ai.rect.centerx - player.rect.centerx) ** 2 + (
            ai.rect.centery - player.rect.centery) ** 2)) \
                > 300 or missile_tracking:
            ai.visibility = False
            self.ai_detected = False
            self.play_new_contact = True
            if self.play_contact_lost:
                self.sound_contact_lost.play()
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
        pygame.draw.circle(screen, BLUE,
                           (player.rect.centerx, player.rect.centery), 300, 1)
        pygame.draw.circle(screen, BLUE,
                           (player.rect.centerx, player.rect.centery), 1050, 1)

    def main(self):
        """Функция с основным игровым циклом"""
        pygame.init()
        pygame.mixer.init()
        size = WIDTH, HEIGHT
        screen = pygame.display.set_mode(size)
        pause_screen = pygame.display.set_mode(size)
        pygame.display.set_caption("CarrierOps")
        clock = pygame.time.Clock()
        fps = 60

        destination_player = self.player.rect.center
        destination_missile = self.player.rect.center

        # основной игровой цикл
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.pause:
                    if event.button == 1:
                        destination_player = event.pos
                    if event.button == 3:
                        destination_missile = event.pos
                        self.missile = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
            if self.missile:
                self.missile_launch(destination_missile)
                self.missile = False
            goal = self.movement(destination_player, self.player, screen)
            self.base_taken(goal, destination_player)
            self.destination_ai()
            self.fog_of_war(self.ai, self.player, self.bases, screen)
            self.set_pause(screen, pause_screen)
            clock.tick(fps)


if __name__ == '__main__':
    game = Run()
    game.main()