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
        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = pygame.math.Vector2([player.rect.centerx, player.rect.centery])
        self.dir = pygame.math.Vector2((destination[0] - player.rect.centerx,
                                        destination[1] - player.rect.centery)).normalize()

        self.visibility = visibility

        self.ai_x, self.ai_y = ai.rect.center

        # флаги, ответственные за паттерн поиска ракеты
        self.activated = False
        self.turn_one_side = True
        self.turn_another_side = False
        self.first_rotate = True

        self.destination = destination

        # три таймера, отсчитывающие время полета ракеты
        self.ticks = 10
        self.speed = 50
        self.total_ticks = 0

        self.ticks1 = 0
        self.speed1 = 50

        self.ticks2 = 0
        self.speed2 = 50

        self.ai = ai

    # обновление координат ракеты при полете к точке активации ГСН
    def update(self):
        clock1 = pygame.time.Clock()

        if not self.activated:
            if self.ticks1 >= self.speed1:
                self.total_ticks += 1
                self.ticks1 = 0
            clock1.tick(300)
            self.ticks1 += 1

        if self.pos != self.destination:
            self.pos += self.dir * 2
            x = int(self.pos.x)
            y = int(self.pos.y)
            self.rect.center = x, y

        if self.destination[0] - 10 < round(self.pos.x) < self.destination[0] + 10 \
                and self.destination[1] - 10 < round(self.pos.y) < self.destination[1] + 10:
            self.activated = True

        self.aircraft_searching()
        if self.activated:
            self.aircraft_tracking(self.ai)

    # обновление координат ракеты при активации ГСН
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

    # обновление координат ракеты при захвате противника ГСН
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
