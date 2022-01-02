import Settings


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply_rect(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def apply_aircraft(self, obj):
        obj.pos[0] += self.dx
        obj.pos[1] += self.dy
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def apply_missiles(self, obj):
        obj.pos.x += self.dx
        obj.pos.y += self.dy

    def camera_center(self):
        for player in Settings.PLAYER_SPRITE:
            self.dx = -(player.rect.x + player.rect.w // 2 - Settings.WIDTH // 2)
            self.dy = -(player.rect.y + player.rect.h // 2 - Settings.HEIGHT // 2)
