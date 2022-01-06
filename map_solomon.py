import Settings
from Settings import SOLOMON_LAND, SOLOMON_WATERMASK
import pygame


class SolomonLand(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт карты"""
    def __init__(self, visibility, board):
        super().__init__()
        self.image = pygame.transform.scale(SOLOMON_LAND, (
            Settings.CELL_SIZE * board.width,
            Settings.CELL_SIZE * board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(pygame.transform.scale(
            SOLOMON_WATERMASK, (Settings.CELL_SIZE * board.width,
                                Settings.CELL_SIZE * board.height)))
        self.parent_board = board
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

    def update(self):
        """Обновление позиции карты"""

    def new_position(self, cell, top, left):
        """Обновление положения карты при изменении разрешения"""
        self.image = pygame.transform.scale(SOLOMON_LAND, (
            Settings.CELL_SIZE * self.parent_board.width,
            Settings.CELL_SIZE * self.parent_board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.parent_board.left, self.parent_board.top)
        self.mask = pygame.mask.from_surface(pygame.transform.scale(
            SOLOMON_WATERMASK, (
                Settings.CELL_SIZE * self.parent_board.width,
                Settings.CELL_SIZE * self.parent_board.height)))