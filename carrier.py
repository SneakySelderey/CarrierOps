import pygame
from Settings import new_image_size, PLAYER_CARRIER_SHEET, get_pos_in_field, \
    get_pos_in_coords, AI_MASK, PLAYER_MASK
import Settings
from math import atan2
from animated_sprite import AnimatedSprite


class Carrier(AnimatedSprite):
    """Класс, определяющий параметры и спрайт авианосца"""
    def __init__(self, sheet, group):
        super().__init__(sheet, 20, 1, group, Settings.CARRIER_GROUP)
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
        if self.obj == 'player':
            self.mask = pygame.mask.from_surface(new_image_size(PLAYER_MASK))
        else:
            self.mask = pygame.mask.from_surface(new_image_size(AI_MASK))
        #elf.mask = pygame.mask.from_surface(self.image)

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
        pr_x, pr_y = get_pos_in_field(self.prev_pos, cell_size, top, left)
        self.prev_pos = get_pos_in_coords((pr_x, pr_y), top, left)
        self.rect = self.image.get_rect(center=self.prev_pos)
        self.pos = list(self.rect.center)
        if self.obj == 'player':
            self.mask = pygame.mask.from_surface(new_image_size(PLAYER_MASK))
        else:
            self.mask = pygame.mask.from_surface(new_image_size(AI_MASK))
        dest_x, dest_y = get_pos_in_field(self.destination,
                                          cell_size, top, left)
        self.destination = get_pos_in_coords((dest_x, dest_y), top, left)
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

    def data_to_save(self):
        """Возвращает список тех занчений, которые можно сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['frames'], to_save['image'], \
            to_save['mask']
        return to_save