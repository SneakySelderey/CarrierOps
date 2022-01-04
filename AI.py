from random import randint
from Settings import AI_IMAGE, AI_SPRITE
import Settings
from carrier import Carrier
from math import sin, cos


class AI(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(AI_SPRITE, AI_IMAGE)
        self.rect.center = [Settings.WIDTH, randint(40, Settings.HEIGHT - 40)]
        self.pos = list(self.rect.center)
        self.destination = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        if self.pos != self.destination and not self.stop:
            # Обновление кооординат (из полярнйо системы в декартову)
            self.pos[0] = self.pos[0] + Settings.AI_SPEED * cos(
                self.alpha)
            self.pos[1] = self.pos[1] + Settings.AI_SPEED * sin(
                self.alpha)
            self.rect.center = self.pos

        if abs(self.destination[0] - self.rect.centerx) <= 10 and \
                abs(self.destination[1] - self.rect.centery) <= 10:
            self.stop = True

