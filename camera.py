import Settings


class Camera:
    """Класс для камеры"""
    def __init__(self):
        """Зададим начальный сдвиг камеры"""
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
        self.apply_rect(obj)

    def apply_missiles(self, obj):
        """Свинуть ракету на смещенеи камеры"""
        obj.pos.x += self.dx
        obj.pos.y += self.dy
        if Settings.IS_PAUSE:
            self.apply_rect(obj)
