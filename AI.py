from Settings import AI_SPRITE, AI_CARRIER_SHEET, get_bigger_rect
from friendly_missile import Missile
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
        self.destination = list(self.rect.center)

        self.prev_pos = list(self.rect.center)

    def update(self):
        """Обновление позиции объекта"""
        self.left = self.prev_pos[0] > self.pos[0]
        land = list(Settings.BACKGROUND_MAP)[0]
        r = pygame.Rect(land.rect.x, land.rect.y, land.rect.w, land.rect.h)
        if pygame.sprite.collide_mask(self, land) or not all(
                get_bigger_rect(r, 2).collidepoint(point) for point in
                [self.rect.midleft, self.rect.midtop, self.rect.midright,
                    self.rect.midbottom]):
            self.pos = self.prev_pos

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

    def respawn(self):
        self.rect.center = [Settings.LEFT + Settings.AI_START[0] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2,
                            Settings.TOP + Settings.AI_START[1] *
                            Settings.CELL_SIZE + Settings.CELL_SIZE // 2]
        self.pos = list(self.rect.center)
        self.current_health = 100
        self.destination = list(self.rect.center)

        self.prev_pos = list(self.rect.center)
