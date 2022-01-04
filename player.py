import pygame
from random import randint
from Settings import new_coords, ALL_SPRITES, new_image_size, PLAYER_IMAGE, \
    PLAYER_SPRITE, ALL_SPRITES_FOR_SURE
import Settings


class Player(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__(ALL_SPRITES, PLAYER_SPRITE, ALL_SPRITES_FOR_SURE)
        self.image = new_image_size(PLAYER_IMAGE)
        land = list(Settings.BACKGROUND_MAP)[0]
        while True:
            self.rect = self.image.get_rect(center=[
                40, randint(40, Settings.HEIGHT - 40)])
            if not pygame.sprite.collide_mask(self, land):
                break
        self.speedx = self.speedy = 0
        self.radius = Settings.CELL_SIZE * 4
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции игрока"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = new_image_size(PLAYER_IMAGE)
        self.rect = self.image.get_rect(
            topleft=new_coords(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)