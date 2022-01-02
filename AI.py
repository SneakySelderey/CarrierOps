import pygame
from random import randint
from Settings import new_coords, ALL_SPRITES, new_image_size, AI_IMAGE, \
    AI_SPRITE, ALL_SPRITES_FOR_SURE
import Settings


class AI(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт ИИ"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES, AI_SPRITE, ALL_SPRITES_FOR_SURE)
        self.image = new_image_size(AI_IMAGE)
        self.rect = self.image.get_rect(center=[Settings.WIDTH,
                                                randint(0, Settings.HEIGHT)])
        self.speedx = self.speedy = 0
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции спрайта"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(AI_IMAGE)
        self.rect = self.image.get_rect(topleft=new_coords(*self.rect.topleft))
        self.mask = pygame.mask.from_surface(self.image)


