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


class NorwegLand(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт карты"""
    def __init__(self, visibility, board):
        super().__init__()
        self.image = pygame.transform.scale(Settings.NORWEG_LAND, (
            Settings.CELL_SIZE * board.width,
            Settings.CELL_SIZE * board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        self.parent_board = board
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

    def new_position(self, cell, top, left):
        """Обновление положения карты при изменении разрешения"""
        self.image = pygame.transform.scale(Settings.NORWEG_LAND, (
            Settings.CELL_SIZE * self.parent_board.width,
            Settings.CELL_SIZE * self.parent_board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.parent_board.left, self.parent_board.top)
        self.mask = pygame.mask.from_surface(self.image)


class ChinaLand(pygame.sprite.Sprite):
    """Класс, определяющий параметры и спрайт карты"""
    def __init__(self, visibility, board):
        super().__init__()
        self.image = pygame.transform.scale(Settings.CHINA_LAND, (
            Settings.CELL_SIZE * board.width,
            Settings.CELL_SIZE * board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        self.parent_board = board
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

    def new_position(self, cell, top, left):
        """Обновление положения карты при изменении разрешения"""
        self.image = pygame.transform.scale(Settings.CHINA_LAND, (
            Settings.CELL_SIZE * self.parent_board.width,
            Settings.CELL_SIZE * self.parent_board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.parent_board.left, self.parent_board.top)
        self.mask = pygame.mask.from_surface(self.image)


class LandCheck(pygame.sprite.Sprite):
    def __init__(self, visibility, board, run):
        super().__init__()
        self.image = pygame.transform.scale(Settings.LAND_CHECK_IMG, (
            Settings.CELL_SIZE * 0.75, Settings.CELL_SIZE * 0.75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        self.parent_board = board
        Settings.ALL_SPRITES_FOR_SURE.add(self)
        Settings.BACKGROUND_MAP.add(self)

        for x in range(board.width):
            for y in range(board.height):
                self.rect.center = (Settings.CELL_SIZE * x + Settings.CELL_SIZE / 2,
                                    Settings.CELL_SIZE * y + Settings.CELL_SIZE / 2)
                if pygame.sprite.collide_mask(self, run.map):
                    Settings.BOARD[y][x] = 'X'

    def new_position(self, cell, top, left):
        pass
