import pygame
from random import randint
from Settings import BLACK, AI_IMAGE, WIDTH, HEIGHT, CELL_SIZE
import Settings
from Settings import new_coords, ALL_SPRITES, new_image_size


class AI(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт ИИ"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES)
        image = AI_IMAGE
        x, y = image.get_size()
        self.image = pygame.transform.scale(image, (
            x * CELL_SIZE // 70, y * CELL_SIZE // 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH, randint(0, HEIGHT)]
        self.prev_rect = self.rect
        self.speedx = 0
        self.speedy = 0
        self.visibility = visibility

    def update(self):
        """Обновление позиции спрайта"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(AI_IMAGE)
        rect = self.image.get_rect()
        rect.topleft = new_coords(self.rect.x, self.rect.y)
        self.rect = rect
