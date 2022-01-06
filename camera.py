import Settings


class Camera:
    """Класс для камеры"""
    def __init__(self):
        """Зададим начальный сдвиг камеры"""
        self.dx = 0
        self.dy = 0
        self.overall_shift_x = 0
        self.overall_shift_y = 0
        self.centered = False

    def rebase(self):
        """Обновление данных камеры"""
        self.centered = False
        self.dx = 0
        self.dy = 0
        self.overall_shift_x = 0
        self.overall_shift_y = 0

    def apply_rect(self, obj):
        """Сдвинуть объект на смещение камеры"""
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def apply_aircraft(self, obj):
        """Сдвинуть самолет на смещенеи камеры"""
        obj.pos[0] += self.dx
        obj.pos[1] += self.dy
        try:
            obj.prev_pos[0] += self.dx
            obj.prev_pos[1] += self.dy
        except AttributeError:
            pass
        self.apply_rect(obj)

    def apply_missiles(self, obj):
        """Свинуть ракету на смещенеи камеры"""
        obj.pos.x += self.dx
        obj.pos.y += self.dy
        if Settings.IS_PAUSE:
            self.apply_rect(obj)

    def new_position(self):
        """Функция для обновления положения - центровка по игроку"""
        self.dx = self.dy = 0
        self.dx -= list(Settings.PLAYER_SPRITE)[
                         0].rect.centerx - Settings.WIDTH // 2
        self.dy -= list(Settings.PLAYER_SPRITE)[
                         0].rect.centery - Settings.HEIGHT // 2
        self.overall_shift_x = 0
        self.overall_shift_y = 0
        self.centered = True
