import pygame
from math import sqrt, hypot
from Settings import EXPLOSION, MISSILE_FRIENDLY, CELL_SIZE, BLACK
import Settings


class MissileFriendly(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт дружественной
    противокорабельной ракеты"""
    def __init__(self, player, activation, ai, visibility):
        super().__init__()
        image = MISSILE_FRIENDLY
        x, y = image.get_size()
        self.image = pygame.transform.scale(image, (
            x * CELL_SIZE // 70, y * CELL_SIZE // 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = pygame.math.Vector2([player.rect.centerx, player.rect.centery])
        self.dir = pygame.math.Vector2((activation[0] - player.rect.centerx,
                                        activation[1] - player.rect.centery)).normalize()

        self.visibility = visibility

        # флаги, ответственные за паттерн поиска ракеты
        self.activated = False
        self.turn_one_side = True
        self.turn_another_side = False
        self.first_rotate = True

        self.activation = activation

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

        if self.pos != self.activation:
            self.pos += self.dir * 2
            x = int(self.pos.x)
            y = int(self.pos.y)
            self.rect.center = x, y

        if self.activation[0] - 10 < round(self.pos.x) < self.activation[0] + 10 \
                and self.activation[1] - 10 < round(self.pos.y) < self.activation[1] + 10:
            self.activated = True

        self.missile_activation()
        if self.activated:
            self.missile_tracking(self.ai)

        img = MISSILE_FRIENDLY
        x, y = img.get_size()
        self.image = pygame.transform.scale(img, (
            x * Settings.CELL_SIZE // 70, y * Settings.CELL_SIZE // 70))

    # обновление координат ракеты при активации ГСН
    def missile_activation(self):
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
    def missile_tracking(self, ai):
        clock2 = pygame.time.Clock()
        if self.ticks2 >= self.speed2:
            self.total_ticks += 1
            self.ticks2 = 0
        clock2.tick(300)
        self.ticks2 += 1
        try:
            if hypot(self.rect.centerx - ai.rect.centerx, self.rect.centery - ai.rect.centery) <= 150:
                self.dir = pygame.math.Vector2((ai.rect.centerx - self.rect.centerx,
                                                ai.rect.centery - self.rect.centery)).normalize()

            if ai.rect.centerx - 10 < self.rect.centerx < ai.rect.centerx + 10 \
                    and ai.rect.centery - 10 < self.rect.centery < ai.rect.centery + 10:
                self.total_ticks = 10
                EXPLOSION.play()
        except ValueError:
            self.total_ticks = 10
