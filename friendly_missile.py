import pygame
from Settings import new_image_size, EXPLOSION, \
    PLAYER_SPRITE, PLAYER_MISSILES, PLAYER_MISSILE_SHEET, EXPLOSION_SHEET
import Settings
from animated_sprite import AnimatedSprite


class MissileFriendly(AnimatedSprite):
    """Класс, определяющий параметры и спрайт дружественной
    противокорабельной ракеты"""
    def __init__(self, activation, visibility):
        super().__init__(PLAYER_MISSILE_SHEET, 15, 1, PLAYER_MISSILES)
        player = list(PLAYER_SPRITE)[0]
        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = pygame.math.Vector2([player.rect.centerx,
                                        player.rect.centery])
        self.prev_pos = list(self.rect.center)
        self.left = True
        self.radius = Settings.CELL_SIZE * 2
        # Таймеры
        self.ticks = 10
        self.ticks2 = 0
        self.total_ticks = 0
        try:
            self.alpha = pygame.math.Vector2((
                activation[0] - player.rect.centerx,
                activation[1] - player.rect.centery)).normalize()
            self.visibility = visibility
        except ValueError:
            self.total_ticks = 10
            self.alpha = pygame.math.Vector2(0, 0)

        # Флаги, ответственные за паттерн поиска ракеты
        self.activated = False
        self.turn = 0
        self.da_bomb = False
        self.activation = list(activation)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление координат ракеты при полете к точке активации ГСН"""
        self.left = self.prev_pos[0] < self.pos.x
        if not self.activated:
            self.total_ticks += 0.02

        if self.pos != self.activation:
            self.prev_pos = [self.pos.x, self.pos.y]
            self.pos += self.alpha * Settings.MISSILE_SPEED
            self.rect.center = self.pos.x, self.pos.y

        if abs(self.activation[0] - self.rect.centerx) <= 10 and \
                abs(self.activation[1] - self.rect.centery) <= 10:
            #  Если ракета достигла цели
            self.activated = True

        self.missile_activation()
        if self.activated:
            self.missile_tracking()

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.frames[self.cur_frame])
        c_x = (self.rect.centerx - left) / cell_size
        c_y = (self.rect.centery - top) / cell_size
        self.rect = self.image.get_rect(
            center=(left + c_x * Settings.CELL_SIZE,
                    top + c_y * Settings.CELL_SIZE))
        self.pos = pygame.math.Vector2(list(self.rect.center))
        act_x = (self.activation[0] - left) / cell_size
        act_y = (self.activation[1] - top) / cell_size
        self.activation = [left + act_x * Settings.CELL_SIZE,
                           top + act_y * Settings.CELL_SIZE]
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = Settings.CELL_SIZE * 2
        if self.left:
            self.image = pygame.transform.flip(new_image_size(
                self.frames[self.cur_frame]), True, False)
        else:
            self.image = new_image_size(self.frames[self.cur_frame])
        if not self.activated:
            try:
                self.alpha = pygame.math.Vector2(
                    (self.activation[0] - self.pos[0],
                     self.activation[1] - self.pos[1])).normalize()
            except ValueError:
                self.total_ticks = 10

    def missile_activation(self):
        """Обновление координат ракет при активации ГСН"""
        if self.activated:
            if self.ticks >= 100:
                self.total_ticks += 1
                self.ticks = 0
                if self.turn == 0:
                    self.alpha = self.alpha.rotate(-40)
                    self.turn += 1
                elif self.turn == 1:
                    self.alpha = self.alpha.rotate(80)
                    self.turn += 1
                elif self.turn == 2:
                    self.alpha = self.alpha.rotate(-80)
                    self.turn = 1
            self.activation = self.pos + self.alpha * 2
            self.ticks += 1

    def missile_tracking(self):
        """Обновление координат ракеты при захвате противника ГСН"""
        if self.ticks2 >= 100:
            self.total_ticks += 1
            self.ticks2 = 0
        self.ticks2 += 1
        try:
            for ai in Settings.AI_SPRITE:
                if pygame.sprite.collide_circle_ratio(0.35)(self, ai):
                    self.alpha = pygame.math.Vector2(
                        (ai.rect.centerx - self.rect.centerx,
                         ai.rect.centery - self.rect.centery)).normalize()
                if pygame.sprite.collide_mask(self, ai):
                    self.da_bomb = True
                    self.cut_sheet(EXPLOSION_SHEET, 6, 2)
                    self.rect.center = ai.rect.center
                    Settings.PLAYER_MISSILES_HIT += 1
                    EXPLOSION.play()
                    break
        except ValueError:
            self.total_ticks = 10

    def update_frame(self):
        """Установка нового кадра"""
        if not self.da_bomb:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames) if \
                self.cur_frame + 1 != len(self.frames) else 7
            if self.left:
                self.image = pygame.transform.flip(new_image_size(
                    self.frames[self.cur_frame]), True, False)
            else:
                self.image = new_image_size(self.frames[self.cur_frame])
        else:
            try:
                self.cur_frame += 1
                self.image = new_image_size(self.frames[self.cur_frame])
            except IndexError:
                self.total_ticks = 10

    def data_to_save(self):
        """Возвращает значения, которые надо сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['frames'], to_save['image'], \
            to_save['mask']
        return 'friendly', to_save
