import pygame
from math import hypot, sin, cos, atan2
from Settings import new_coords, ALL_SPRITES, new_image_size, \
    AIRCRAFT_FRIENDLY, LANDING, PLAYER_SPRITE
import Settings
from numba import njit
R = 2


class AircraftFriendly(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт самолета"""
    def __init__(self, player, destination, ai, visibility):
        super().__init__(ALL_SPRITES)
        self.image = new_image_size(AIRCRAFT_FRIENDLY)
        self.rect = self.image.get_rect(center=[player.rect.centerx,
                                                player.rect.centery])
        self.pos = list(self.rect.center)
        self.visibility = visibility
        self.alpha = atan2(destination[1] - self.pos[1],
                           destination[0] - self.pos[0])
        self.total_ticks = 0  # Общее число тиков
        self.ai = ai
        self.destination = destination  # Направление движения
        self.to_player = False  # Если самолет возвращается на авианосец
        self.stop = False  # Если самолет достиг точки направления
        self.delete = False  # Если самолет вернулся на авианосец, он удаляется

    def update(self):
        """Обновление координат самолета при полете"""
        self.total_ticks += 1

        if self.pos != self.destination and not self.stop:
            self.pos[0] = self.pos[0] + R * cos(self.alpha)
            self.pos[1] = self.pos[1] + R * sin(self.alpha)
            self.rect.center = self.pos

        if abs(self.destination[0] - self.rect.centerx) <= 10 and \
                abs(self.destination[1] - self.rect.centery) <= 10:
            self.stop = True

        if self.total_ticks >= 1500:
            self.aircraft_return()
        else:
            self.aircraft_tracking(self.ai)

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(AIRCRAFT_FRIENDLY)
        rect = self.image.get_rect()
        rect.x, rect.y = new_coords(self.rect.x, self.rect.y)
        self.rect = rect
        self.ai.rect.center = new_coords(*self.ai.rect.center)
        self.pos = [*new_coords(self.pos[0], self.pos[1])]
        self.destination = new_coords(*self.destination)
        self.alpha = atan2(self.destination[1] - self.rect.centery,
                           self.destination[0] - self.rect.centerx)

    def aircraft_return(self):
        """Обновление координат при возвращении на авианосец"""
        player = list(PLAYER_SPRITE)[0]
        self.alpha = atan2(player.rect.centery - self.rect.centery,
                           player.rect.centerx - self.rect.centerx)
        self.destination = player.rect.centerx, player.rect.centery
        self.to_player = True
        self.stop = False
        if self.alpha == 0:
            LANDING.play()
            self.delete = True

    def aircraft_tracking(self, ai):
        """Обновление координат при слежении за целью"""
        self.ai.rect.center = ai.rect.center
        dist_to_ai = hypot(self.ai.rect.centerx - self.rect.centerx,
                            self.ai.rect.centery - self.rect.centery)
        if dist_to_ai <= Settings.CELL_SIZE * 3.5:
            self.alpha = atan2(self.ai.rect.centery - self.rect.centery,
                               self.ai.rect.centerx - self.rect.centerx)
            self.stop = False