import Settings
import pygame


class SolomonLand(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт карты"""
    def __init__(self, visibility):
        super().__init__()
        self.image = pygame.transform.scale(Settings.SOLOMON_LAND, (Settings.WIDTH * 2, Settings.HEIGHT * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

    def update(self):
        """Обновление позиции карты"""


class MovePoint(pygame.sprite.Sprite):
    def __init__(self, visibility):
        super().__init__()
        self.image = Settings.new_image_size(Settings.MOVE_POINT)
        self.rect = self.image.get_rect()
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.MOVE_POINT_SPRITE.add(self)


class SolomonWater(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт карты"""
    def __init__(self, visibility):
        super().__init__()
        self.image = pygame.transform.scale(Settings.SOLOMON_WATER, (Settings.WIDTH * 2, Settings.HEIGHT * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

    def update(self):
        """Обновление позиции карты"""
        pass
