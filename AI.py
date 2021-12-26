import pygame
from random import randint
from Settings import BLACK, AI_IMAGE, WIDTH, HEIGHT


class AI(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт ИИ"""
    def __init__(self, visibility):
        super().__init__()
        self.image = AI_IMAGE
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH, randint(0, HEIGHT)]
        self.speedx = 0
        self.speedy = 0
        self.visibility = visibility

    def update(self):
        """Обновление позиции спрайта"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy