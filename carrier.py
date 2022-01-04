import pygame
from random import randint
from Settings import ALL_SPRITES, new_image_size, PLAYER_IMAGE, \
    PLAYER_SPRITE, ALL_SPRITES_FOR_SURE, AI_SPRITE, AI_IMAGE, CARRIER_GROP
import Settings


class Carrier(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    Data = {'player': [PLAYER_SPRITE, PLAYER_IMAGE, True],
            'ai': [AI_SPRITE, AI_IMAGE, False]}

    def __init__(self, obj):
        super().__init__(ALL_SPRITES, ALL_SPRITES_FOR_SURE,
                         Carrier.Data[obj][0], CARRIER_GROP)
        self.image = new_image_size(Carrier.Data[obj][1])
        if obj == 'player':
            self.rect = self.image.get_rect(center=[
                40, randint(40, Settings.HEIGHT - 40)])
        else:
            self.rect = self.image.get_rect(center=[
                Settings.WIDTH, randint(40, Settings.HEIGHT - 40)])
        self.obj = obj
        self.speedx = self.speedy = 0
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = Carrier.Data[obj][2]
        self.health_capacity = 100
        self.current_health = 100
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции игрока"""
        if Settings.OIL_VOLUME:
            self.rect.x += self.speedx
            self.rect.y += self.speedy

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(Carrier.Data[self.obj][1])
        c_x = (self.rect.centerx - left) // cell_size
        c_y = (self.rect.centery - top) // cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.mask = pygame.mask.from_surface(self.image)