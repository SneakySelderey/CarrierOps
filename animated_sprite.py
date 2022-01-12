import pygame
import Settings
from random import choice
from Settings import new_image_size, EXPLOSION_SHEET, WATER_COLORS, FIRE_COLORS


class AnimatedSprite(pygame.sprite.Sprite):
    """Класс для анимированного спрайта"""
    def __init__(self, sheet, columns, rows, *groups):
        """Инициализация. Принимает картинку, кличество столбцов и строк и
        группы спарйтов, где должен быть объект"""
        super().__init__(Settings.ALL_SPRITES_FOR_SURE,
                         Settings.ANIMATED_SPRTIES, *groups)
        self.frames = self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = new_image_size(self.frames[self.cur_frame])

    def cut_sheet(self, sheet, columns, rows):
        """Функция для создания отдельных кадрос из листа"""
        self.cur_frame = 0
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        return [sheet.subsurface(pygame.Rect(
            (self.rect.w * i, self.rect.h * j), self.rect.size)) for j in
            range(rows) for i in range(columns)]

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = new_image_size(self.frames[self.cur_frame])


class Explosion(AnimatedSprite):
    """Класс для взрыва"""
    def __init__(self, carrier):
        """Инициализация. Принимает авианосец-родитель"""
        self.parent = carrier
        self.visibility = True
        super().__init__(EXPLOSION_SHEET, 6, 2, Settings.EXPLOSION_GROUP)
        self.rect = self.image.get_rect(center=carrier.rect.center)

    def update(self):
        """Обновление положения"""
        self.rect.center = self.parent.rect.center

    def update_frame(self):
        """Установка нового кадра"""
        try:
            self.cur_frame += 1
            self.image = new_image_size(self.frames[self.cur_frame])
        except IndexError:
            self.kill()

    def new_position(self, cell, top, left):
        self.image = new_image_size(self.frames[self.cur_frame])
        self.rect = self.image.get_rect(center=self.parent.rect.center)


class Particle(pygame.sprite.Sprite):
    """Класс для частицы"""
    Sizes = [15, 25, 35]
    Values = {'carrier': (WATER_COLORS, range(-2, 2), range(-6, 6),
                          [-Settings.CELL_SIZE / 80, 0]),
              'missile': (FIRE_COLORS, range(-2, 2), range(-80, 80),
                          [-Settings.CELL_SIZE / 80, 0])}

    def __init__(self, parent):
        """Инициализация. Принимает эммитер"""
        super().__init__(Settings.PARTICLES_GROUP)
        self.obj = 'carrier' if parent in Settings.CARRIER_GROUP else 'missile'
        colors, dx, dy, gravity = self.Values[self.obj]
        gravity[0] = -Settings.CELL_SIZE / 80 if not parent.left else \
            Settings.CELL_SIZE / 80
        size = choice(self.Sizes)
        self.image = pygame.Surface((Settings.CELL_SIZE // size,
                                     Settings.CELL_SIZE // size))
        self.image.fill(choice(colors))
        self.parent = parent
        self.rect = self.image.get_rect(center=self.parent.rect.center)
        if parent.left:
            self.rect.x += int(0.25 * parent.rect.w)
        else:
            self.rect.x -= int(0.25 * parent.rect.w)
        if self.obj == 'carrier':
            self.rect.y = parent.rect.y + int(0.8 * parent.rect.h)
        else:
            self.rect.y = parent.rect.midright[1]
        self.velocity = [choice(dx) * Settings.CELL_SIZE / 1000,
                         choice(dy) * Settings.CELL_SIZE / 1000]
        self.gravity = list(gravity)
        self.prev_left = parent.left
        self.visibility = True
        self.ticks = 7

    def update(self):
        """Обновление положения, движение"""
        if self.obj == 'missile':
            self.rect.y = self.parent.rect.midright[1]
        if self.prev_left != self.parent.left:
            self.gravity[0] = -self.gravity[0]
        self.ticks -= 1
        if self.parent.left:
            self.velocity[0] += self.gravity[0]
            self.velocity[1] += self.gravity[1]
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        else:
            self.velocity[0] -= self.gravity[0]
            self.velocity[1] -= self.gravity[1]
            self.rect.x -= self.velocity[0]
            self.rect.y -= self.velocity[1]
        self.prev_left = self.parent.left
        if not self.ticks:
            self.kill()