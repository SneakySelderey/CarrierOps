import pygame
from random import randint
from Settings import BLACK, PLAYER_IMAGE, HEIGHT


class Player(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__()
        self.image = PLAYER_IMAGE
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [40, randint(40, HEIGHT - 40)]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

    def update(self):
        """Обновление позиции игрока"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy