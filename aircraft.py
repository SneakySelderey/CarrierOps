import pygame
from math import hypot
from Settings import new_coords, ALL_SPRITES, new_image_size, \
    AIRCRAFT_FRIENDLY, LANDING
import Settings
import numpy as np
np.seterr(divide='ignore', invalid='ignore')


class AircraftFriendly(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт самолета"""
    def __init__(self, player, destination, ai, visibility):
        super().__init__(ALL_SPRITES)
        self.image = new_image_size(AIRCRAFT_FRIENDLY)
        self.rect = self.image.get_rect()
        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = np.array([*self.rect.center])
        self.dir = np.array([destination[0] - self.rect.centerx,
                             destination[1] - self.rect.centery])
        self.dir = self.dir / np.linalg.norm(self.dir)

        self.visibility = visibility

        self.playerx, self.playery = player.rect.centerx, player.rect.centery
        self.ai_x, self.ai_y = ai.rect.center

        # три таймера, отсчитывающие время полета самолета

        self.ticks1 = 0
        self.speed1 = 50
        self.total_ticks = 0

        self.player = player
        self.ai = ai
        self.destination = destination
        self.stop = False
        self.delete = False
        self.play_sound = True

    # обновление координат самолета при полете к маршрутной точке
    def update(self):
        clock1 = pygame.time.Clock()

        if self.ticks1 >= self.speed1:
            self.total_ticks += 1
            self.ticks1 = 0
        clock1.tick(300)
        self.ticks1 += 1

        if list(self.pos) != self.destination and not self.stop:
            self.pos = self.pos + self.dir * 2
            x = self.pos[0]
            y = self.pos[1]
            self.rect.center = x, y

        delta = Settings.CELL_SIZE // 10
        if self.destination[0] - 10 - delta < self.rect.centerx < self.destination[0] + 10 + delta\
                and self.destination[1] - 10 - delta < self.rect.centery < self.destination[1] + 10 + delta:
            self.stop = True

        if self.total_ticks >= 30:
            self.aircraft_return(self.player)
        else:
            self.aircraft_tracking(self.ai)

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(AIRCRAFT_FRIENDLY)
        rect = self.image.get_rect()
        rect.x, rect.y = new_coords(self.rect.x, self.rect.y)
        self.rect = rect
        self.player.rect.center = new_coords(*self.player.rect.center)
        self.ai.rect.center = new_coords(*self.ai.rect.center)
        self.pos = np.array([*new_coords(self.pos[0], self.pos[1])])
        self.destination = new_coords(*self.destination)
        x, y = new_coords(self.destination[0] - self.rect.centerx,
                          self.destination[1] - self.rect.centery)
        try:
            self.dir = np.array([x, y])
            self.dir = self.dir / np.linalg.norm(self.dir)
        except ValueError:
            self.delete = True

    def aircraft_return(self, player):
        try:
            self.dir = np.array([player.rect.centerx - self.rect.centerx,
                                player.rect.centery - self.rect.centery])
            self.dir = self.dir / np.linalg.norm(self.dir)
            self.destination = player.rect.centerx, player.rect.centery
            self.stop = False
            if self.play_sound:
                LANDING.play()
                self.play_sound = False
        except ValueError:
            self.delete = True

    # обновление координат самолета при слежении за целью
    def aircraft_tracking(self, ai):
        self.ai_x, self.ai_y = ai.rect.center
        try:
            dist_between_air_ai = hypot(self.ai_x - self.rect.centerx,
                                        self.ai_y - self.rect.centery)
            if dist_between_air_ai <= Settings.CELL_SIZE * 3.5:
                self.dir = np.array([self.ai_x - self.rect.centerx,
                                     self.ai_y - self.rect.centery])
                self.dir = self.dir / np.linalg.norm(self.dir)
                self.stop = False
        except ValueError:
            pass
