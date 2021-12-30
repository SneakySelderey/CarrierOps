import pygame
from math import hypot
from Settings import AIRCRAFT_FRIENDLY, CELL_SIZE, LANDING, BLACK
import Settings


class AircraftFriendly(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт самолета"""
    def __init__(self, player, destination, ai, visibility):
        super().__init__()
        image = AIRCRAFT_FRIENDLY
        x, y = image.get_size()
        self.image = pygame.transform.scale(image, (
            x * CELL_SIZE // 70, y * CELL_SIZE // 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = pygame.math.Vector2([player.rect.centerx, player.rect.centery])
        self.dir = pygame.math.Vector2((destination[0] - player.rect.centerx,
                                        destination[1] - player.rect.centery)).normalize()

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
        self.landing = LANDING

    # обновление координат самолета при полете к маршрутной точке
    def update(self):
        clock1 = pygame.time.Clock()

        if self.ticks1 >= self.speed1:
            self.total_ticks += 1
            self.ticks1 = 0
        clock1.tick(300)
        self.ticks1 += 1

        if self.pos != self.destination and not self.stop:
            self.pos += self.dir * 2
            x = int(self.pos.x)
            y = int(self.pos.y)
            self.rect.center = x, y

        if self.destination[0] - 10 < self.rect.centerx < self.destination[0] + 10 \
                and self.destination[1] - 10 < self.rect.centery < self.destination[1]:
            self.stop = True

        if self.total_ticks >= 30:
            self.aircraft_return(self.player)
        else:
            self.aircraft_tracking(self.ai)

        image = AIRCRAFT_FRIENDLY
        x, y = image.get_size()
        self.image = pygame.transform.scale(image, (
            x * Settings.CELL_SIZE // 70, y * Settings.CELL_SIZE // 70))

    def aircraft_return(self, player):
        try:
            self.dir = pygame.math.Vector2((player.rect.centerx - self.rect.centerx,
                                           player.rect.centery - self.rect.centery)).normalize()
            self.destination = player.rect.centerx, player.rect.centery
            self.stop = False
            if self.play_sound:
                self.landing.play()
                self.play_sound = False
        except ValueError:
            self.delete = True

    # обновление координат самолета при слежении за целью
    def aircraft_tracking(self, ai):
        self.ai_x, self.ai_y = ai.rect.center
        try:
            dist_between_air_ai = hypot(self.ai_x - self.rect.centerx, self.ai_y - self.rect.centery)
            if dist_between_air_ai <= 250:
                self.dir = pygame.math.Vector2((self.ai_x - self.rect.centerx,
                                                self.ai_y - self.rect.centery)).normalize()
                self.stop = False
        except ValueError:
            pass
