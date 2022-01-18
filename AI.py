from Settings import AI_SPRITE, AI_CARRIER_SHEET, get_pos_in_coords, \
    get_pos_in_field
from missile import Missile
import Settings
from carrier import Carrier
from math import sin, cos, hypot
from animated_sprite import Particle
from Settings import bfs
from collections import deque
import pygame


class AI(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(AI_CARRIER_SHEET, AI_SPRITE)
        self.rect.center = [Settings.AI_START[0] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2, Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.path = []
        self.destination = list(self.rect.center)
        self.prev_pos = list(self.rect.center)
        self.num_of_missiles = 1

    def update(self):
        """Обновление позиции объекта"""
        if self.oil_volume:
            self.left = self.prev_pos[0] > self.pos[0]
            land = list(Settings.BACKGROUND_MAP)[0]
            if pygame.sprite.collide_mask(self, land):
                self.pos = [self.prev_pos[0], self.prev_pos[1]]
                self.check_stuck()
                self.path = []

            if self.pos != self.destination and not self.stop:
                self.prev_pos = [self.pos[0], self.pos[1]]
                # Обновление кооординат (из полярной системы в декартову)
                self.pos[0] = self.pos[0] + Settings.AI_SPEED * cos(
                    self.alpha)
                self.pos[1] = self.pos[1] + Settings.AI_SPEED * sin(
                    self.alpha)
                self.rect.center = self.pos
            if abs(self.destination[0] - self.rect.centerx) <= 5 and abs(
                    self.destination[1] - self.rect.centery) <= 5:
                self.stop = True
            if self.stop:
                pygame.time.set_timer(Settings.AI_FUEL_CONSUMPTION, 0)
            if not self.stop and self.visibility:
                [Particle(self) for _ in range(2)]

            if not self.num_of_missiles or not self.num_of_aircraft or \
                    self.current_health < 30 or self.oil_volume < 35:
                bases = [base for base in Settings.BASES_SPRITES if
                         base.state == 'ai']
                if bases:
                    to_return = None
                    if len(bases) == 1:
                        if self.check_base_for_resources(bases[0]):
                            to_return = bases[0]
                    else:
                        bases.sort(key=lambda x: hypot(
                            self.rect.centery - x.rect.centery,
                            self.rect.centerx - x.rect.centerx))
                        if self.check_base_for_resources(bases[0]):
                            to_return = bases[0]
                        elif self.check_base_for_resources(bases[1]):
                            to_return = bases[1]
                    if to_return is not None:
                        ai_pos_x, ai_pos_y = map(int, get_pos_in_field(
                            self.rect.center, Settings.CELL_SIZE, Settings.TOP,
                            Settings.LEFT))
                        self.path = deque(bfs(
                            (ai_pos_y, ai_pos_x), (to_return.y, to_return.x)))
                        path = self.path.popleft()
                        self.new_destination(get_pos_in_coords(
                            [path[1] + 0.5, path[0] + 0.5], Settings.TOP,
                            Settings.LEFT))

    def check_base_for_resources(self, base):
        """Функция проверки базы на наличие ресурсов"""
        if base.num_of_missiles or base.num_of_aircraft or \
            base.oil_volume - self.oil_volume >= 35 or \
                base.num_of_repair_parts * 10 > self.current_health:
            return True
        return False

    def missile_launch(self, coords):
        """Функция для запуска ракеты"""
        if self.num_of_missiles > 0:
            mis = Missile(self.rect.center, coords, False, 'ai')
            mis.new_position(Settings.CELL_SIZE, Settings.TOP, Settings.LEFT)
            self.num_of_missiles -= 1
        for i in Settings.BASES_SPRITES:
            if i.state == 'ai':
                i.num_of_missiles = 100

    def respawn(self):
        """Возрождение авианосца потивника"""
        self.rect.center = [Settings.LEFT + Settings.AI_START[0] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2,
                            Settings.TOP + Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.current_health = 100
        self.destination = list(self.rect.center)
        self.prev_pos = list(self.rect.center)
        self.num_of_missiles = 5
        self.num_of_aircraft = 3
        self.oil_volume = 100
