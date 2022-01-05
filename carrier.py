import pygame
from Settings import ALL_SPRITES, new_image_size, PLAYER_IMAGE, \
    PLAYER_SPRITE, ALL_SPRITES_FOR_SURE, AI_SPRITE, AI_IMAGE, CARRIER_GROP
import Settings
from math import atan2


class Carrier(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт авианосца"""
    Data = {'player': [PLAYER_SPRITE, PLAYER_IMAGE, True],
            'ai': [AI_SPRITE, AI_IMAGE, False]}

    def __init__(self, group, img):
        super().__init__(ALL_SPRITES, ALL_SPRITES_FOR_SURE,
                         group, CARRIER_GROP)
        self.obj_img = img
        self.image = new_image_size(img)
        self.rect = self.image.get_rect()
        self.pos = list(self.rect.center)
        self.destination = self.pos
        self.alpha = 0
        self.stop = False
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = True if img == PLAYER_IMAGE else False
        self.health_capacity = 100
        self.current_health = 100
        self.mask = pygame.mask.from_surface(self.image)

    def new_destination(self, pos):
        """Функция для задания новой точки направления"""
        self.stop = False
        self.destination = list(pos)
        self.alpha = atan2(self.destination[1] - self.pos[1],
                           self.destination[0] - self.pos[0])
        if self.alpha != 0 and self.obj_img == PLAYER_IMAGE:
            pygame.time.set_timer(Settings.FUEL_CONSUMPTION,
                                  Settings.FUEL_CONSUMPTION_SPEED)

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.obj_img)
        c_x = (self.rect.centerx - left) // cell_size
        c_y = (self.rect.centery - top) // cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.pos = list(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        dest_x = (self.destination[0] - left) // cell_size
        dest_y = (self.destination[1] - top) // cell_size
        self.destination = [left + dest_x * Settings.CELL_SIZE,
                            top + dest_y * Settings.CELL_SIZE]
        self.alpha = atan2(self.destination[1] - self.pos[1],
                           self.destination[0] - self.pos[0])
        self.radius = Settings.CELL_SIZE * 4