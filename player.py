import pygame
from Settings import PLAYER_SPRITE, PLAYER_CARRIER_SHEET, get_bigger_rect
import Settings
from carrier import Carrier
from math import sin, cos, atan2
from animated_sprite import Particle
import copy


class Player(Carrier):
    """Класс авианосца игрока"""
    def __init__(self):
        super().__init__(PLAYER_CARRIER_SHEET, PLAYER_SPRITE)
        self.rect.center = [Settings.PLAYER_START[0] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2,
                            Settings.PLAYER_START[1] * Settings.CELL_SIZE +
                            Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.destination = list(self.rect.center)
        self.prev_pos = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        self.left = self.prev_pos[0] > self.pos[0]
        if Settings.OIL_VOLUME:
            land = list(Settings.BACKGROUND_MAP)[0]
            r = pygame.Rect(land.rect.x, land.rect.y, land.rect.w, land.rect.h)
            if pygame.sprite.collide_mask(self, land) or not all(
                get_bigger_rect(r, 2).collidepoint(point) for point in
                [self.rect.midleft, self.rect.midtop, self.rect.midright,
                    self.rect.midbottom]):
                self.pos = self.prev_pos

            if self.pos != self.destination and not self.stop:
                self.prev_pos = list(copy.copy(self.pos))
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

            if not self.stop:
                [Particle(self) for _ in range(4)]