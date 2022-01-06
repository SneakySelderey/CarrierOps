import pygame
from Settings import ALL_SPRITES, new_image_size, EXPLOSION, \
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
        self.radius = Settings.CELL_SIZE * 2
        # Таймеры
        self.ticks = 10
        self.ticks2 = 0
        self.total_ticks = 0
        try:
            self.alpha = pygame.math.Vector2((
                activation[0] - player.rect.centerx,
                activation[1] - player.rect.centery)).normalize()
            self.visibility = visibility
        except ValueError:
            self.total_ticks = 20
            self.alpha = pygame.math.Vector2(0, 0)

        # Флаги, ответственные за паттерн поиска ракеты
        self.activated = False
        self.turn = 0
        self.activation = list(activation)
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

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(MISSILE_FRIENDLY)
        c_x = (self.rect.centerx - left) / cell_size
        c_y = (self.rect.centery - top) / cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.pos = pygame.math.Vector2(list(self.rect.center))
        act_x = (self.activation[0] - left) / cell_size
        act_y = (self.activation[1] - top) / cell_size
        self.activation = [left + act_x * Settings.CELL_SIZE,
                           top + act_y * Settings.CELL_SIZE]
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = Settings.CELL_SIZE * 2
        if not self.activated:
            try:
                self.alpha = pygame.math.Vector2(
                    (self.activation[0] - self.pos[0],
                     self.activation[1] - self.pos[1])).normalize()
            except ValueError:
                self.total_ticks = 20

    def missile_activation(self):
        """Обновление координат ракет при активации ГСН"""
        if self.activated:
            if self.ticks >= 100:
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
        if self.ticks2 >= 100:
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
