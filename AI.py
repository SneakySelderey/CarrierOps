from Settings import AI_SPRITE, AI_CARRIER_SHEET
from missile import Missile
import Settings
from carrier import Carrier
from math import sin, cos
from animated_sprite import Particle
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

    def update(self):
        """Обновление позиции объекта"""
        self.left = self.prev_pos[0] > self.pos[0]
        land = list(Settings.BACKGROUND_MAP)[0]
        if pygame.sprite.collide_mask(self, land):
            self.pos = [self.prev_pos[0], self.prev_pos[1]]

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
        if not self.stop and self.visibility:
            [Particle(self) for _ in range(2)]

    def missile_launch(self, coords):
        """Функция для запуска ракеты"""
        mis = Missile(self.rect.center, coords, False, 'ai')
        mis.new_position(Settings.CELL_SIZE, Settings.TOP, Settings.LEFT)

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
