import pygame
from Settings import BLACK, BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, \
    ALL_SPRITES
import Settings


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE}

    def __init__(self, x, y, state, visibility, cell_size):
        super().__init__(ALL_SPRITES)
        base_img = pygame.transform.scale(Base.Images[state],
                                          (cell_size, cell_size))
        self.x, self.y = x, y
        self.size = cell_size
        self.image = base_img
        self.state = state
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x * cell_size, y * cell_size]
        self.visibility = visibility

    def update(self, *args):
        """Обновление изображения базы, если она захватывается"""
        if args and Base.Images[args[0]] != self.image:
            self.state = args[0]
            self.image = pygame.transform.scale(Base.Images[args[0]],
                                                (self.size, self.size))

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.size = Settings.CELL_SIZE
        self.rect.topleft = [self.x * self.size, self.y * self.size]
        self.image = pygame.transform.scale(Base.Images[self.state],
                                            (self.size, self.size))
