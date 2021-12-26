import pygame
from Settings import BLACK, BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    def __init__(self, x, y, state, visibility, cell_size):
        super().__init__()
        if state == 'neutral':
            base_img = BASE_NEUTRAL.convert()
        elif state == 'friendly':
            base_img = BASE_FRIENDLY.convert()
        else:
            base_img = BASE_HOSTILE.convert()
        self.image = base_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x + cell_size // 2, y + cell_size // 2]

        self.visibility = visibility
