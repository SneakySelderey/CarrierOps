import pygame
from Settings import new_coords, ALL_SPRITES, new_image_size, EXPLOSION, \
    MISSILE_FRIENDLY, PLAYER_SPRITE, PLAYER_MISSILES, \
    ALL_SPRITES_FOR_SURE
import Settings


class MissileFriendly(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт дружественной
    противокорабельной ракеты"""
    def __init__(self, activation, visibility):
        super().__init__(ALL_SPRITES, PLAYER_MISSILES, ALL_SPRITES_FOR_SURE)
        player = list(PLAYER_SPRITE)[0]
        self.image = new_image_size(MISSILE_FRIENDLY)
        self.rect = self.image.get_rect(center=[player.rect.centerx,
                                                player.rect.centery])
        self.pos = pygame.math.Vector2([player.rect.centerx,
                                        player.rect.centery])
        # Таймеры
        self.ticks = 10
        self.ticks2 = 0
        self.total_ticks = 0
        try:
            self.alpha = pygame.math.Vector2((
                activation[0] - player.rect.centerx,
                activation[1] - player.rect.centery)).normalize()
            self.visibility = visibility
            self.radius = Settings.CELL_SIZE * 2
        except ValueError:
            self.total_ticks = 10
            self.alpha = pygame.math.Vector2(0, 0)

        # Флаги, ответственные за паттерн поиска ракеты
        self.activated = False
        self.turn = 0
        self.activation = activation
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление координат ракеты при полете к точке активации ГСН"""
        if not self.activated:
            self.total_ticks += 0.02

        if self.pos != self.activation:
            self.pos += self.alpha * Settings.MISSILE_SPEED
            self.rect.center = self.pos.x, self.pos.y

        if abs(self.activation[0] - self.rect.centerx) <= 10 and \
                abs(self.activation[1] - self.rect.centery) <= 10:
            #  Если ракета достигла цели
            self.activated = True

        self.missile_activation()
        if self.activated:
            self.missile_tracking()

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(MISSILE_FRIENDLY)
        rect = self.image.get_rect()
        rect.x, rect.y = new_coords(self.rect.x, self.rect.y)
        self.rect = rect
        self.pos = [*new_coords(self.pos[0], self.pos[1])]
        self.activation = new_coords(*self.activation)
        self.mask = pygame.mask.from_surface(self.image)
        if not self.activated:
            try:
                x, y = new_coords(self.activation[0] - self.pos[0],
                                  self.activation[1] - self.pos[1])
                self.alpha = pygame.math.Vector2((x, y)).normalize()
            except ValueError:
                self.total_ticks = 10

    def missile_activation(self):
        """Обновление координат ракет при активации ГСН"""
        if self.activated:
            if self.ticks >= 50:
                self.total_ticks += 1
                self.ticks = 0
                if self.turn == 0:
                    self.alpha = self.alpha.rotate(-40)
                    self.turn += 1
                elif self.turn == 1:
                    self.alpha = self.alpha.rotate(80)
                    self.turn += 1
                elif self.turn == 2:
                    self.alpha = self.alpha.rotate(-80)
                    self.turn = 1
            self.activation = self.pos + self.alpha * 2
            self.ticks += 1

    def missile_tracking(self):
        """Обновление координат ракеты при захвате противника ГСН"""
        if self.ticks2 >= 50:
            self.total_ticks += 1
            self.ticks2 = 0
        self.ticks2 += 1
        try:
            for ai in Settings.AI_SPRITE:
                if pygame.sprite.collide_circle_ratio(0.35)(self, ai):
                    self.alpha = pygame.math.Vector2(
                        (ai.rect.centerx - self.rect.centerx,
                         ai.rect.centery - self.rect.centery)).normalize()
                if pygame.sprite.collide_mask(self, ai):
                    self.rect = self.rect.move(0, 1)
                    self.total_ticks = 10
                    EXPLOSION.play()
                    break
        except ValueError:
            self.total_ticks = 10
