import pygame
from Settings import BLACK, BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL


class Base(pygame.sprite.Sprite):
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE}
    """Класс, определяющий спрайт и местоположение базы-острова"""
    def __init__(self, x, y, state, visibility, cell_size):
        super().__init__()
        base_img = pygame.transform.scale(Base.Images[state],
                                          (cell_size, cell_size))
        self.size = cell_size
        self.image = base_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x + cell_size // 2, y + cell_size // 2]
        self.visibility = visibility

    def update(self, *args):
        """Обновление изображения базы, если она захватывается"""
        if args and Base.Images[args[0]] != self.image:
            self.image = pygame.transform.scale(Base.Images[args[0]],
                                          (self.size, self.size))
