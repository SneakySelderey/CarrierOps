import pygame
from Settings import new_image_size, EXPLOSION, \
    PLAYER_SPRITE, PLAYER_MISSILES, PLAYER_MISSILE_SHEET, \
    get_pos_in_coords, get_pos_in_field
import Settings
from animated_sprite import AnimatedSprite, Explosion, Particle


class MissileFriendly(AnimatedSprite):
    """Класс, определяющий параметры и спрайт дружественной
    противокорабельной ракеты"""
    def __init__(self, activation, visibility, obj, base, run):
        if obj in Settings.PLAYER_SPRITE:
            super().__init__(PLAYER_MISSILE_SHEET, 15, 1, PLAYER_MISSILES)
            player = list(PLAYER_SPRITE)[0]
        else:
            super().__init__(Settings.HOSTILE_MISSILE_SHEET, 15, 1, Settings.AI_MISSILES)
            player = list(Settings.AI_SPRITE)[list(Settings.AI_SPRITE).index(obj)]
        self.rect.center = [player.rect.centerx, player.rect.centery]
        self.pos = pygame.math.Vector2([player.rect.centerx,
                                        player.rect.centery])
        self.prev_pos = list(self.rect.center)
        self.left = False
        self.radius = Settings.CELL_SIZE * 2
        self.pause_checked = False
        self.activation_on_base = True
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
        self.activation = list(activation)
        self.mask = pygame.mask.from_surface(self.image)
        self.obj = obj
        self.base = base
        self.run = run

    def update(self):
        """Обновление координат ракеты при полете к точке активации ГСН"""
        # если ракета исчерпала свой ресурс, она падает в море и
        # спрайт удаляется
        if self.total_ticks >= 10:
            Settings.ANIMATED_SPRTIES.remove(self)
            Settings.PLAYER_MISSILES.remove(self)
            Settings.AI_MISSILES.remove(self)
            Settings.ALL_SPRITES_FOR_SURE.remove(self)

        self.left = self.prev_pos[0] > self.pos.x

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

        if self.base:
            if self.activation_on_base:
                if pygame.sprite.collide_circle_ratio(2)(self, self.base):
                    self.activated = True
            else:
                if pygame.sprite.collide_circle_ratio(1)(self, self.base):
                    self.activated = True

        [Particle(self) for _ in range(15)]

        self.missile_activation()
        if self.activated:
            self.missile_tracking()

    def new_position(self, cell_size, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(self.frames[self.cur_frame])
        c_x, c_y = get_pos_in_field(self.rect.center, cell_size, top, left)
        self.rect = self.image.get_rect(
            center=get_pos_in_coords((c_x, c_y), top, left))
        self.pos = pygame.math.Vector2(list(self.rect.center))
        pr_x, pr_y = get_pos_in_field(self.prev_pos, cell_size, top, left)
        self.prev_pos = get_pos_in_coords((pr_x, pr_y), top, left)
        act_x, act_y = get_pos_in_field(self.activation, cell_size, top, left)
        self.activation = get_pos_in_coords((act_x, act_y), top, left)
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = Settings.CELL_SIZE * 2
        self.left = self.prev_pos[0] > self.pos.x
        if not self.left:
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
            if self.obj in Settings.PLAYER_SPRITE:
                for ai in Settings.AI_SPRITE:
                if pygame.sprite.collide_circle_ratio(0.35)(self, ai):
                    self.alpha = pygame.math.Vector2(
                        (ai.rect.centerx - self.rect.centerx,
                         ai.rect.centery - self.rect.centery)).normalize()
                if pygame.sprite.collide_mask(self, ai):
                    Explosion(ai)
                    Settings.PLAYER_MISSILES_HIT += 1
                    EXPLOSION.play()
                    break
            else:
                for player in Settings.PLAYER_SPRITE:
                    if pygame.sprite.collide_circle_ratio(0.35)(self, player):
                    self.alpha = pygame.math.Vector2(
                        (player.rect.centerx - self.rect.centerx,
                         player.rect.centery - self.rect.centery)).normalize()
                if pygame.sprite.collide_mask(self, player):
                    Explosion(player)
                    Settings.AI_MISSILES_HIT += 1
                    EXPLOSION.play()
                    break
        except ValueError:
            self.total_ticks = 10

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames) if \
            self.cur_frame + 1 != len(self.frames) else 7
        if not self.left:
            self.image = pygame.transform.flip(new_image_size(
                self.frames[self.cur_frame]), True, False)
        else:
            self.image = new_image_size(self.frames[self.cur_frame])

    def data_to_save(self):
        """Возвращает значения, которые надо сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['frames'], to_save['image'], \
            to_save['mask']
        return 'friendly', to_save
