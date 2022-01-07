import pygame
from math import sin, cos, atan2, degrees
from Settings import new_image_size, LANDING, PLAYER_SPRITE, PLAYER_AIRCRAFT, \
    AIRCRAFT_FRIENDLY_SHEET
import Settings
from animated_sprite import AnimatedSprite


class AircraftFriendly(AnimatedSprite):
    """Класс, определяющий параметры и спрайт самолета"""
    def __init__(self, destination, visibility):
        super().__init__(AIRCRAFT_FRIENDLY_SHEET, 7, 1, PLAYER_AIRCRAFT)
        player = list(PLAYER_SPRITE)[0]
        self.rect = self.image.get_rect(center=[player.rect.centerx,
                                                player.rect.centery])
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
        self.radius = Settings.CELL_SIZE * 3.5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление координат самолета при полете"""
        if not self.delete:
            self.total_ticks += 1

            if self.pos != self.destination and not self.stop:
                # Обновление кооординат (из полярнйо системы в декартову)
                self.pos[0] = self.pos[0] + Settings.AIR_SPEED * cos(self.alpha)
                self.pos[1] = self.pos[1] + Settings.AIR_SPEED * sin(self.alpha)
                self.rect.center = self.pos

            if abs(self.destination[0] - self.rect.centerx) <= 10 and \
                    abs(self.destination[1] - self.rect.centery) <= 10:
                #  Если самолет достиг цели
                self.stop = True

            if self.total_ticks >= 1500:
                self.aircraft_return()
            else:
                self.aircraft_tracking()

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.frames[self.cur_frame])
        c_x = (self.rect.centerx - left) / cell_size
        c_y = (self.rect.centery - top) / cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.pos = list(self.rect.center)
        dest_x = (self.destination[0] - left) / cell_size
        dest_y = (self.destination[1] - top) / cell_size
        self.destination = [left + dest_x * Settings.CELL_SIZE,
                            top + dest_y * Settings.CELL_SIZE]
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
        player = list(PLAYER_SPRITE)[0]
        self.alpha = atan2(player.rect.centery - self.rect.centery,
                           player.rect.centerx - self.rect.centerx)
        self.destination = [player.rect.centerx, player.rect.centery]
        self.stop = False
        if pygame.sprite.collide_rect(self, player):
            Settings.NUM_OF_AIRCRAFT += 1
            self.delete = True

    def aircraft_tracking(self):
        """Обновление координат при слежении за целью"""
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_circle_ratio(0.47)(self, ai):
                self.stop = False
                if not pygame.sprite.collide_mask(self, ai):
                    self.alpha = atan2(ai.rect.centery - self.rect.centery,
                                       ai.rect.centerx - self.rect.centerx)
                break

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.rotate(new_image_size(
            self.frames[self.cur_frame]), -degrees(self.alpha)-90)
