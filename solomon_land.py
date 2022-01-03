import Settings
import pygame


class SolomonLand(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт игрока"""
    def __init__(self, visibility):
        super().__init__(Settings.ALL_SPRITES, Settings.PLAYER_SPRITE, Settings.ALL_SPRITES_FOR_SURE)
        self.image = pygame.transform.scale(Settings.SOLOMON_LAND, (Settings.WIDTH, Settings.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление позиции карты"""
        pass
