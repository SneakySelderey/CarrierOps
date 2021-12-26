import pygame
from Settings import BLACK, AI_IMAGE


class AI(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт ИИ"""
    def __init__(self, board, visibility, cell_size):
        super().__init__()
        self.image = AI_IMAGE.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [cell_size * board.width, cell_size * board.height]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

    def update(self):
        """Обновление позиции спрайта"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy