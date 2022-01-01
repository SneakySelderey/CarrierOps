import pygame
from random import randint
from Settings import new_coords, ALL_SPRITES, new_image_size, PLAYER_IMAGE, \
    PLAYER_SPRITE
import Settings


class Player(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES, PLAYER_SPRITE)
        self.image = new_image_size(PLAYER_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = [40, randint(40, Settings.HEIGHT - 40)]
        self.speedx = 0
        self.speedy = 0

        Settings.PLAYER_SPRITE.add(self)

        self.visibility = visibility

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции игрока"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(PLAYER_IMAGE)
        rect = self.image.get_rect()
        rect.topleft = new_coords(self.rect.x, self.rect.y)
        self.rect = rect