import pygame
import Settings
from random import choice
from Settings import new_image_size, EXPLOSION_SHEET, BLUE, DEEPBLUE, \
    DARKBLUE, BRILLIANTBLUE


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
        pass



class Particle(pygame.sprite.Sprite):
    """Класс для частицы"""
    def __init__(self, parent, dx, dy, image, gravity):
        """Инициализация. Принимает эммитер, измененеи скорости по x и y,
        изображение и гравитацию (кортеж из чисел по обеим осям) и направление
         двжиения частиц"""
        super().__init__(Settings.PARTICLES_GROUP)
        self.images = [pygame.transform.scale(image, (scale, scale)) for
                       scale in [Settings.CELL_SIZE // 15,
                                 Settings.CELL_SIZE // 25,
                                 Settings.CELL_SIZE // 35]]
        self.parent = parent
        self.image = choice(self.images)
        self.rect = self.image.get_rect(center=self.parent.rect.center)
        self.velocity = [dx, dy]
        self.gravity = list(gravity)
        self.prev_left = False
        self.visibility = True
        self.ticks = 5

    def update(self):
        """Обновление положения, движение"""
        if self.prev_left != self.parent.left:
            self.gravity[0] = -self.gravity[1]
            w = self.parent.image.get_width() // 4
            x = self.parent.rect.bottomleft[0] if not self.parent.left else \
                self.parent.rect.bottomright[0]
            self.rect.x = x + w if not self.parent.left else x - w
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
        if not self.rect.colliderect(list(Settings.BACKGROUND_MAP)[0]) or \
                not self.ticks:
            self.kill()


class WaterParticle(Particle):
    """Класс для частицы воды"""
    Colors = [BLUE, BRILLIANTBLUE, DARKBLUE, DEEPBLUE]

    def __init__(self, parent):
        surface = pygame.Surface((Settings.CELL_SIZE // 15,
                                 Settings.CELL_SIZE // 15))
        surface.fill(choice(self.Colors))
        super().__init__(parent, choice(range(-2, 2)), choice(range(-2, 2)),
                         surface, (-1, 0))
        self.rect.x, self.rect.y = parent.rect.bottomright if parent.left \
            else parent.rect.bottomleft
        w = self.parent.image.get_width() // 4
        h = self.parent.image.get_height() // 4
        x, y = self.rect.x, self.rect.y
        self.rect.x = x + w if not self.parent.left else x - w
        self.rect.y = y - h
