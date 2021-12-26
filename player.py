import pygame
from Settings import BLACK, PLAYER_IMAGE


class Player(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__()
        self.image = PLAYER_IMAGE.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [25, 25]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

    def update(self):
        """Обновление позиции игрока"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy