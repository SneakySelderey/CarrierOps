import pygame
import random
from math import sqrt
from board import Board
from player import Player
from AI import AI
from base import Base
from friendly_missile import MissileFriendly
from Settings import *


# класс, в котором обрабатываются все основные игровые события
class Run:
    def __init__(self):
        pass

    # пуск противокорабельной ракеты
    def missile_launch(self, destination, player, bases, ai):
        self.friendly_missiles.append(MissileFriendly(player, True, destination, ai, True, self.sound_explosion))

        self.sound_fire_VLS.play()

    # движение игрока или ИИ
    def movement(self, destination, game_obj, screen=None):
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

    # расчет точки движения для ИИ
    def destination_ai(self, bases, ai, player, fps):
        # if (sqrt((player.rect.centerx - ai.rect.centerx) ** 2 + (player.rect.centery - ai.rect.centery) ** 2)) \
        #         <= 300:
        #     dest = self.movement_ai([player.rect.centerx, player.rect.centery], ai, fps)
        #     self.battle = True
        # else:
        distance = []
        ai_pos_x = ai.rect.centerx // self.cell_size
        ai_pos_y = ai.rect.centery // self.cell_size
        for i in range(len(bases)):
            base_x = bases[i].rect.centerx // self.cell_size
            base_y = bases[i].rect.centery // self.cell_size
            dist = [ai_pos_x - base_x, ai_pos_y - base_y]
            if [base_x, base_y] not in self.hostile_bases:
                distance.append(
                    (dist, [bases[i].rect.centerx, bases[i].rect.centery]))
        try:
            destination_ai = min(distance)
            idx = distance.index(destination_ai)
            dest = self.movement(distance[idx][1], ai)
            self.base_lost(dest, distance[idx][1], bases)
        except ValueError:
            self.running = False
            print('Вы проиграли!')

    # база захвачена союзником
    def base_taken(self, dest, destination, bases, player, ai):
        if dest[0] and dest[1]:
            player_grid_x = destination[0] // self.cell_size
            player_grid_y = destination[1] // self.cell_size
            for i in range(len(bases)):
                if bases[i].rect.centerx // self.cell_size == player_grid_x and bases[i].rect.centery // \
                        self.cell_size == player_grid_y:
                    bases[i] = Base(bases[i].rect.centerx - self.cell_size // 2, bases[i].rect.centery - self.cell_size
                                    // 2, 'friendly', True, self.cell_size)
                    if [bases[i].rect.centerx // self.cell_size, bases[i].rect.centery // self.cell_size] in \
                            self.hostile_bases:
                        self.hostile_bases.remove([bases[i].rect.centerx // self.cell_size, bases[i].rect.centery //
                                                   self.cell_size])

    # база захвачена противником
    def base_lost(self, dest, destination, bases):
        if dest[0] and dest[1]:
            ai_grid_x = destination[0] // self.cell_size
            ai_grid_y = destination[1] // self.cell_size
            for i in range(len(bases)):
                if bases[i].rect.centerx // self.cell_size == ai_grid_x and bases[i].rect.centery // self.cell_size == \
                        ai_grid_y:
                    bases[i] = Base(bases[i].rect.centerx - self.cell_size // 2, bases[i].rect.centery -
                                    self.cell_size // 2, 'hostile', True, self.cell_size)
                    self.hostile_bases.append([bases[i].rect.centerx // self.cell_size, bases[i].rect.centery //
                                               self.cell_size])

    # поставить игру на паузу
    def set_pause(self, screen, pause_screen, board, size, ai):
        if not self.pause:
            self.all_sprites.update()
            if not self.ai_detected:
                ai.update()
            pygame.display.flip()
            screen.fill(GRAY5)
            self.all_sprites.draw(screen)
            board.render(screen)
        else:
            self.all_sprites.draw(screen)
            sc_text = MAIN_FONT.render('PAUSE', True, WHITE)
            pos = sc_text.get_rect(center=(size[0] // 2, size[1] // 2))
            pause_screen.blit(sc_text, pos)
            pygame.display.flip()

    # отрисовка тумана войны
    def fog_of_war(self, ai, player, bases, screen):
        # если противник обнаружен ракетой
        missile_tracking = False
        for missile in self.friendly_missiles:
            # если цель в радиусе обнаружения ракеты, то поднимается соответствующий флаг
            if (sqrt((missile.rect.centerx - ai.rect.centerx) ** 2 + (missile.rect.centery - ai.rect.centery) ** 2)) \
                    <= 150:
                missile_tracking = True
            # если ракета исчерпала свой ресурс, она падает в море и спрайт удаляется
            if missile.total_ticks >= 10:
                self.friendly_missiles.remove(missile)
                self.all_sprites.remove(missile)
            # отрисовка радиуса обнаружения ракеты
            if not missile.activated:
                pygame.draw.line(screen, BLUE, (missile.rect.centerx, missile.rect.centery),
                                 (missile.activation[0], missile.activation[1]))
            pygame.draw.circle(screen, BLUE, (missile.rect.centerx, missile.rect.centery), 150, 1)

        # отрисовка спрайта противника
        if (sqrt((ai.rect.centerx - player.rect.centerx) ** 2 + (ai.rect.centery - player.rect.centery) ** 2)) \
                <= 300 or missile_tracking:
            ai.visibility = True
            pygame.draw.circle(screen, RED, (ai.rect.centerx, ai.rect.centery), 300, 1)
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
        elif (sqrt((ai.rect.centerx - player.rect.centerx) ** 2 + (ai.rect.centery - player.rect.centery) ** 2)) \
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
        pygame.draw.circle(screen, BLUE, (player.rect.centerx, player.rect.centery), 300, 1)
        pygame.draw.circle(screen, BLUE, (player.rect.centerx, player.rect.centery), 1050, 1)

    # функция с основным игровым циклом
    def main(self):
        pygame.init()
        pygame.mixer.init()
        size = WIDTH, HEIGHT
        screen = pygame.display.set_mode(size)
        pause_screen = pygame.display.set_mode(size)
        pygame.display.set_caption("CarrierOps")
        clock = pygame.time.Clock()

        self.cell_size = 75
        self.cells_x = size[0] // self.cell_size
        self.cells_y = size[1] // self.cell_size
        board = Board(self.cells_x, self.cells_y, Run())
        board.set_view(0, 0, self.cell_size)

        fps = 60

        # добавление спрайтов в группы
        self.all_sprites = pygame.sprite.Group()
        player = Player(True)
        bases = []
        self.friendly_missiles = []
        self.hostile_missiles = []
        for i in range(10):
            x = random.randint(0, self.cells_x - 1) * self.cell_size
            y = random.randint(0, self.cells_y - 1) * self.cell_size
            bases.append(Base(x, y, 'neutral', True, self.cell_size))
        ai = AI(board, False, self.cell_size)

        # различные флаги
        destination_player = player.rect.center
        self.running = True
        self.pause = False
        start = True
        self.hostile_bases = []
        self.ai_detected = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False
        self.missile = False

        # озвучка событий
        self.sound_new_contact = NEW_CONTACT
        self.sound_contact_lost = CONTACT_LOST
        self.sound_fire_VLS = FIRE_VLS
        self.sound_weapon_acquire = WEAPON_ACQUIRE
        self.sound_explosion = EXPLOSION

        self.list_all_sprites = [player, ai, bases, self.friendly_missiles, self.hostile_missiles]

        # основной игровой цикл
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        destination_player = event.pos
                    if event.button == 3:
                        destination_missile = event.pos
                        self.missile = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause

            if self.missile:
                self.missile_launch(destination_missile, player, bases, ai)
                self.missile = False

            dest = self.movement(destination_player, player, screen)

            self.base_taken(dest, destination_player, bases, player, ai)

            self.destination_ai(bases, ai, player, fps)

            self.fog_of_war(ai, player, bases, screen)

            clock.tick(fps)

            self.set_pause(screen, pause_screen, board, size, ai)

            if start:
                self.pause = True
                start = False


if __name__ == '__main__':
    Run().main()