import pygame
from Settings import new_image_size, PLAYER_CARRIER_SHEET
import Settings
from math import atan2
from animated_sprite import AnimatedSprite


class Carrier(AnimatedSprite):
    """Класс, определяющий параметры и спрайт авианосца"""
    def __init__(self, sheet, group):
        super().__init__(sheet, 20, 1, group)
        self.obj = 'player' if sheet == PLAYER_CARRIER_SHEET else 'ai'
        self.pos = list(self.rect.center)
        self.destination = self.pos
        self.alpha = 0
        self.stop = False
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = True if sheet == PLAYER_CARRIER_SHEET else False
        self.health_capacity = 100
        self.current_health = 100
        self.prev_pos = list(self.rect.center)
        self.left = False
        self.mask = pygame.mask.from_surface(self.image)

    def new_destination(self, pos):
        """Функция для задания новой точки направления"""
        self.stop = False
        self.destination = list(pos)
        self.alpha = atan2(self.destination[1] - self.pos[1],
                           self.destination[0] - self.pos[0])
        if self.alpha != 0 and self.obj == 'player':
            pygame.time.set_timer(Settings.FUEL_CONSUMPTION,
                                  Settings.FUEL_CONSUMPTION_SPEED)

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.frames[self.cur_frame])
        c_x = (self.rect.centerx - left) / cell_size
        c_y = (self.rect.centery - top) / cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.pos = list(self.rect.center)
        self.prev_pos = [self.pos[0], self.pos[1]]
        self.mask = pygame.mask.from_surface(self.image)
        dest_x = (self.destination[0] - left) / cell_size
        dest_y = (self.destination[1] - top) / cell_size
        self.destination = [left + dest_x * Settings.CELL_SIZE,
                            top + dest_y * Settings.CELL_SIZE]
        self.alpha = atan2(self.destination[1] - self.pos[1],
                           self.destination[0] - self.pos[0])
        if self.left:
            self.image = pygame.transform.flip(new_image_size(
                self.frames[self.cur_frame]), True, False)
        else:
            self.image = new_image_size(self.frames[self.cur_frame])
        self.radius = Settings.CELL_SIZE * 4

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.left:
            self.image = pygame.transform.flip(new_image_size(
                self.frames[self.cur_frame]), True, False)
        else:
            self.image = new_image_size(self.frames[self.cur_frame])