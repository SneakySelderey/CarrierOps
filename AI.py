from Settings import AI_SPRITE, AI_CARRIER_SHEET
from missile import Missile
from aircraft import Aircraft
import Settings
from carrier import Carrier
from math import sin, cos
from animated_sprite import Particle
import pygame
import copy


class AI(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(AI_CARRIER_SHEET, AI_SPRITE)
        self.rect.center = [Settings.AI_START[0] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2, Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.idx = f'A{list(Settings.AI_SPRITE).index(self)}'
        self.destination = list(self.rect.center)

        self.prev_pos = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        self.left = self.prev_pos[0] > self.pos[0]
        land = list(Settings.BACKGROUND_MAP)[0]
        if pygame.sprite.collide_mask(self, land):
            self.pos = [self.prev_pos[0], self.prev_pos[1]]
        elif not all(land.rect.collidepoint(point) for point in
                     self.get_points()):
            for i in [(0, -3), (0, 3), (3, 0), (-3, 0)]:
                self.rect.center = self.rect.center[0] + i[0], \
                                   self.rect.center[1] + i[1]
                self.pos = list(self.rect.center)
                if all(land.rect.collidepoint(point) for point in
                       self.get_points()):
                    break

        if self.pos != self.destination and not self.stop:
            self.prev_pos = list(copy.copy(self.pos))
            # Обновление кооординат (из полярной системы в декартову)
            self.pos[0] = self.pos[0] + Settings.AI_SPEED * cos(
                self.alpha)
            self.pos[1] = self.pos[1] + Settings.AI_SPEED * sin(
                self.alpha)
            self.rect.center = self.pos
        if not self.stop and self.visibility:
            [Particle(self) for _ in range(2)]

        if self.current_health <= 0:
            self.respawn()

    def missile_launch(self, coords):
        """Функция для запуска ракеты"""
        mis = Missile(self.rect.center, coords, False, 'ai')
        mis.new_position(Settings.CELL_SIZE, Settings.TOP, Settings.LEFT)

    def air_launch(self, coords):
        """Функция для запуска самолета"""
        player = list(Settings.PLAYER_SPRITE)[0]
        if not any(pygame.sprite.collide_mask(air, player) for air in
                   Settings.AI_AIRCRAFT):
            air = Aircraft(self.rect.center, coords, False, self.idx)
            air.new_position(Settings.CELL_SIZE, Settings.TOP, Settings.LEFT)

    def respawn(self):
        [aircraft.kill() for aircraft in Settings.AI_AIRCRAFT if
         aircraft.obj == self.idx]
        self.rect.center = [Settings.LEFT + Settings.AI_START[0] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2,
                            Settings.TOP + Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.current_health = 100
        self.destination = list(self.rect.center)

        self.prev_pos = list(self.rect.center)
