import pygame
from random import randint
from Settings import PLAYER_IMAGE, PLAYER_SPRITE
import Settings
from carrier import Carrier
from math import sin, cos, atan2


class Player(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(PLAYER_SPRITE, PLAYER_IMAGE)
        self.rect.center = [Settings.PLAYER_START[0] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2,
                            Settings.PLAYER_START[1] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.destination = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        if Settings.OIL_VOLUME:
            if self.pos != self.destination and not self.stop:
                # Обновление кооординат (из полярнйо системы в декартову)
                self.pos[0] = self.pos[0] + Settings.PLAYER_SPEED * cos(
                    self.alpha)
                self.pos[1] = self.pos[1] + Settings.PLAYER_SPEED * sin(
                    self.alpha)
                self.rect.center = self.pos

            if abs(self.destination[0] - self.rect.centerx) <= 10 and \
                    abs(self.destination[1] - self.rect.centery) <= 10:
                self.stop = True

            if self.stop:
                pygame.time.set_timer(Settings.FUEL_CONSUMPTION, 0)

            self.alpha = atan2(self.destination[1] - self.pos[1],
                               self.destination[0] - self.pos[0])