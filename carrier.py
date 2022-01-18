import pygame
from Settings import new_image_size, PLAYER_CARRIER_SHEET, get_pos_in_field, \
    get_pos_in_coords, find_free_space
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
        self.stop = True
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = True if sheet == PLAYER_CARRIER_SHEET else False
        self.health_capacity = 100
        self.current_health = 100
        self.prev_pos = list(self.rect.center)
        self.left = False
        self.mask = pygame.mask.from_surface(new_image_size(
            self.frames[self.cur_frame]))
        self.num_of_missiles = 5
        self.num_of_aircraft = 3
        self.oil_volume = 100

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
        if not self.stop:
            self.pos = get_pos_in_coords(get_pos_in_field(
                self.pos, cell_size, top, left), top, left)
        else:
            self.pos = list(self.rect.center)
        self.left = self.prev_pos[0] > self.pos[0]
        self.mask = pygame.mask.from_surface(new_image_size(
            self.frames[self.cur_frame]))
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

    def get_points(self):
        """Возвращает середины сторон прямоугольника авианосца"""
        return [self.rect.midleft, self.rect.midtop, self.rect.midright,
                self.rect.midbottom]

    def get_pos(self):
        """Функция дя получения точки - положения в сетке для BFS"""
        pos_x, pos_y = map(int, get_pos_in_field(
            self.rect.center, Settings.CELL_SIZE, Settings.TOP,
            Settings.LEFT))
        return pos_y, pos_x

    def check_stuck(self):
        """Функция для перемещения авианосца, если он застрял в суше"""
        land = list(Settings.BACKGROUND_MAP)[0]
        if pygame.sprite.collide_mask(self, land):
            x = [(self.rect.x + i, self.rect.centery) for i in
                 range(1, self.image.get_width() - 1)]
            y = [(self.rect.centerx, self.rect.y + i) for i in
                 range(1, self.image.get_height() - 1)]
            a = filter(
                lambda p: land.rect.collidepoint(p) and land.mask.get_at(p),
                set(x) | set(y))
            if a:
                p = find_free_space(self.get_pos())
                self.destination = list(get_pos_in_coords([
                    p[1] + 0.5, p[0] + 0.5], Settings.TOP, Settings.LEFT))
                for i in [(3, 0), (-3, 0), (0, 3), (0, -3)]:
                    self.rect.center = self.rect.center[0] + i[0], \
                                       self.rect.center[1] + i[1]
                    self.pos = list(self.rect.center)
                    if not pygame.sprite.collide_mask(self, land):
                        break

