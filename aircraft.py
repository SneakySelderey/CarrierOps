from math import hypot
from Settings import *


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
        self.pos = (player.rect.centerx, player.rect.centery)
        self.destination = destination
        self.rect.center = self.pos

        self.visibility = visibility

        self.ai_x, self.ai_y = ai.rect.center

        self.k = (self.destination[1] - self.pos[1]) / (self.destination[0] - self.pos[0])
        self.b = self.pos[1] - self.k * self.pos[0]

        # флаги, ответственные за паттерн поиска самолета
        self.activated = False
        self.turn_one_side = True
        self.turn_another_side = False
        self.first_rotate = True

        # три таймера, отсчитывающие время полета самолета
        self.ticks = 10
        self.speed = 50
        self.total_ticks = 0

        self.ticks1 = 0
        self.speed1 = 50

        self.ticks2 = 0
        self.speed2 = 50

        self.ai = ai

    # обновление координат самолета при полете к маршрутной точке
    def update(self):
        clock1 = pygame.time.Clock()

        if not self.activated:
            if self.ticks1 >= self.speed1:
                self.total_ticks += 1
                self.ticks1 = 0
            clock1.tick(300)
            self.ticks1 += 1

        if self.pos != self.destination:
            self.pos = self.pos[0] + 1, self.k * (self.pos[0] + 1) + self.b
            self.rect.center = self.pos

        if self.destination[0] - 10 < round(self.pos[0]) < self.destination[0] + 10 \
                and self.destination[1] - 10 < round(self.pos[1]) < self.destination[1] + 10:
            self.activated = True

        self.aircraft_searching()
        if self.activated:
            self.aircraft_tracking(self.ai)

    # обновление координат самолета при поиске цели
    def aircraft_searching(self):
        clock = pygame.time.Clock()
        if self.activated:
            if self.ticks >= self.speed:
                self.total_ticks += 1
                self.ticks = 0
                if self.first_rotate:
                    self.dir = self.dir.rotate(-40)
                    self.first_rotate = False
                elif self.turn_one_side:
                    self.dir = self.dir.rotate(80)
                    self.first_rotate = False
                    self.turn_one_side = False
                    self.turn_another_side = True
                elif self.turn_another_side:
                    self.dir = self.dir.rotate(-80)
                    self.turn_one_side = True
                    self.turn_another_side = False
            clock.tick(300)
            self.ticks += 1

    # обновление координат самолета при слежении за целью
    def aircraft_tracking(self, ai):
        self.ai_x, self.ai_y = ai.rect.center

        clock2 = pygame.time.Clock()
        if self.ticks2 >= self.speed2:
            self.total_ticks += 1
            self.ticks2 = 0
        clock2.tick(300)
        self.ticks2 += 1
        try:
            dist_between_air_ai = hypot(self.ai_x - self.rect.centerx, self.ai_y - self.rect.centery)
            if dist_between_air_ai <= 500:
                self.dir = pygame.math.Vector2((ai.rect.centerx - self.rect.centerx,
                                                ai.rect.centery - self.rect.centery)).normalize()

            if ai.rect.centerx - 10 < self.rect.centerx < ai.rect.centerx + 10 \
                    and ai.rect.centery - 10 < self.rect.centery < ai.rect.centery + 10:
                self.total_ticks = 10
        except ValueError:
            self.total_ticks = 10
