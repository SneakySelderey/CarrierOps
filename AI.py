from Settings import AI_IMAGE, AI_SPRITE, NEIGHBOURS
import Settings
from carrier import Carrier
from math import sin, cos
import pygame


class AI(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(AI_SPRITE, AI_IMAGE)
        self.rect.center = [Settings.AI_START[0] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2, Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.destination = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        land = list(Settings.BACKGROUND_MAP)[0]
        if pygame.sprite.collide_mask(self, land):
            for i in NEIGHBOURS:
                self.rect.center = self.rect.center[0] + i[0], \
                                   self.rect.center[1] + i[1]
                self.pos = list(self.rect.center)
                if not pygame.sprite.collide_mask(self, land):
                    break
        if self.pos != self.destination and not self.stop:
            # Обновление кооординат (из полярной системы в декартову)
            self.pos[0] = self.pos[0] + Settings.AI_SPEED * cos(
                self.alpha)
            self.pos[1] = self.pos[1] + Settings.AI_SPEED * sin(
                self.alpha)
            self.rect.center = self.pos

