import pygame
from random import randint
from Settings import BLACK, PLAYER_IMAGE, HEIGHT, CELL_SIZE
import Settings
from Settings import new_coords, ALL_SPRITES, new_image_size


class Player(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES)
        image = PLAYER_IMAGE
        x, y = image.get_size()
        self.image = pygame.transform.scale(image, (
            x * CELL_SIZE // 70, y * CELL_SIZE // 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [40, randint(40, HEIGHT - 40)]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

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