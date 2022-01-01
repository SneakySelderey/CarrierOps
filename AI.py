import pygame
from random import randint
from Settings import new_coords, ALL_SPRITES, new_image_size, AI_IMAGE, AI_SPRITE
import Settings


class AI(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт ИИ"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES, AI_SPRITE)
        self.image = new_image_size(AI_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = [Settings.WIDTH, randint(0, Settings.HEIGHT)]
        self.prev_rect = self.rect
        self.speedx = 0
        self.speedy = 0

        Settings.AI_SPRITE.add(self)

        self.visibility = visibility

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции спрайта"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(AI_IMAGE)
        rect = self.image.get_rect()
        rect.topleft = new_coords(*self.rect.topleft)
        self.rect = rect


