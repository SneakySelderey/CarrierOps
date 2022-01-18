import pygame
from math import sin, cos, atan2, degrees
from Settings import new_image_size, LANDING, PLAYER_SPRITE, PLAYER_AIRCRAFT, \
    AIRCRAFT_FRIENDLY_SHEET, get_pos_in_coords, get_pos_in_field
import Settings
from animated_sprite import AnimatedSprite


class Aircraft(AnimatedSprite):
    """Класс, определяющий параметры и спрайт самолета"""
    def __init__(self, center, destination, visibility, obj):
        self.obj = obj
        if self.obj == 'P0':
            super().__init__(AIRCRAFT_FRIENDLY_SHEET, 7, 1, PLAYER_AIRCRAFT)
        else:
            super().__init__(Settings.AIRCRAFT_HOSTILE_SHEET, 7, 1, Settings.AI_AIRCRAFT)
        self.rect.center = center
        self.pos = list(self.rect.center)
        self.visibility = visibility
        self.alpha = atan2(destination[1] - self.pos[1],
                           destination[0] - self.pos[0])
        self.image = pygame.transform.rotate(self.image,
                                             -degrees(self.alpha))
        self.total_ticks = 0  # Общее число тиков
        self.destination = list(destination)  # Направление движения
        self.stop = False  # Если самолет достиг точки направления
        self.delete = False  # Если самолет вернулся на авианосец, он удаляется
        self.play_sound = True
        self.to_return = False
        self.tracking = True
        self.radius = Settings.CELL_SIZE * 3.5
        self.mask = pygame.mask.from_surface(self.image)
        self.pause_checked = False

    def update(self):
        """Обновление координат самолета при полете"""
        land = list(Settings.BACKGROUND_MAP)[0]
        if not all(
                land.rect.collidepoint(point) for point in [
                    self.rect.midleft, self.rect.midtop, self.rect.midright,
                    self.rect.midbottom]) and not self.to_return:
            self.stop = True

        if not self.delete:
            self.total_ticks += 1

            if self.pos != self.destination and not self.stop:
                # Обновление кооординат (из полярнйо системы в декартову)
                self.pos[0] = self.pos[0] + Settings.AIR_SPEED * cos(
                    self.alpha)
                self.pos[1] = self.pos[1] + Settings.AIR_SPEED * sin(
                    self.alpha)
                self.rect.center = self.pos

            if abs(self.destination[0] - self.rect.centerx) <= 5 and \
                    abs(self.destination[1] - self.rect.centery) <= 5 and \
                    not self.tracking:
                #  Если самолет достиг цели
                self.stop = True

            if self.total_ticks >= 1500:
                self.aircraft_return()
            else:
                self.aircraft_tracking()

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.frames[self.cur_frame])
        c_x, c_y = get_pos_in_field(self.rect.center, cell_size, top, left)
        self.rect = self.image.get_rect(
            center=get_pos_in_coords((c_x, c_y), top, left))
        self.pos = list(self.rect.center)
        dest_x, dest_y = get_pos_in_field(self.destination, cell_size, top,
                                          left)
        self.destination = get_pos_in_coords((dest_x, dest_y), top, left)
        if not self.stop:
            self.alpha = atan2(self.destination[1] - self.rect.centery,
                               self.destination[0] - self.rect.centerx)
        self.image = pygame.transform.rotate(self.image,
                                             -degrees(self.alpha) - 90)
        self.radius = Settings.CELL_SIZE * 3.5

    def aircraft_return(self):
        """Обновление координат при возвращении на авианосец"""
        if self.play_sound:
            LANDING.play()
            self.play_sound = False
        carrier = list(Settings.PLAYER_SPRITE)[0] if self.obj == 'P0' else [
            i for i in Settings.AI_SPRITE if i.idx == self.obj][0]
        self.alpha = atan2(carrier.rect.centery - self.rect.centery,
                           carrier.rect.centerx - self.rect.centerx)
        self.destination = [carrier.rect.centerx, carrier.rect.centery]
        self.stop = False
        self.to_return = True
        if pygame.sprite.collide_rect(self, carrier):
            Settings.NUM_OF_AIRCRAFT += 1
            self.delete = True

    def aircraft_tracking(self):
        """Обновление координат при слежении за целью"""
        if self.obj == 'P0':
            opposite = list(Settings.AI_SPRITE)
        else:
            opposite = list(Settings.PLAYER_SPRITE)
        for target in opposite:
            if pygame.sprite.collide_circle_ratio(0.47)(self, target):
                self.tracking = True
                self.stop = False
                if not pygame.sprite.collide_mask(self, target):
                    self.alpha = atan2(target.rect.centery - self.rect.centery,
                                       target.rect.centerx - self.rect.centerx)
                break

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.rotate(new_image_size(
            self.frames[self.cur_frame]), -degrees(self.alpha)-90)

    def data_to_save(self):
        """Возвраащет значения для сохранения"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['frames'], to_save['image'], \
            to_save['mask']
        return 'friendly', to_save
