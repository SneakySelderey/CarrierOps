import Settings
from Settings import SOLOMON_LAND, NORWEG_LAND, CHINA_LAND
import pygame


class Map(pygame.sprite.Sprite):
    Pictures = {'solomon': SOLOMON_LAND,
                'norweg': NORWEG_LAND,
                'china': CHINA_LAND}

    def __init__(self, visibility, board, chosen_map):
        super().__init__(Settings.ALL_SPRITES_FOR_SURE,
                         Settings.BACKGROUND_MAP)
        self.image = pygame.transform.scale(Map.Pictures[chosen_map], (
            Settings.CELL_SIZE * board.width,
            Settings.CELL_SIZE * board.height))
        self.rect = self.image.get_rect(topleft=(board.left, board.top))
        self.visibility = visibility,
        self.parent_board = board
        self.chosen_map = chosen_map
        self.mask = pygame.mask.from_surface(self.image)

    def new_position(self, cell, top, left):
        """Обновление положения карты при изменении разрешения"""
        self.image = pygame.transform.scale(Map.Pictures[self.chosen_map], (
            Settings.CELL_SIZE * self.parent_board.width,
            Settings.CELL_SIZE * self.parent_board.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.parent_board.left, self.parent_board.top)
        self.mask = pygame.mask.from_surface(self.image)

    def data_to_save(self):
        """Возвращает значения, которые надо сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['image'], to_save['mask'], \
            to_save['parent_board']
        return to_save


class LandCheck(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.image = pygame.transform.scale(Settings.LAND_CHECK_IMG, (
            Settings.CELL_SIZE * 0.6, Settings.CELL_SIZE * 0.6))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)

        Settings.BOARD = [['.' for _ in range(board.width)]
                          for _ in range(board.height)]

        for x in range(board.width):
            for y in range(board.height):
                self.rect.center = (Settings.CELL_SIZE * x + Settings.CELL_SIZE / 2,
                                    Settings.CELL_SIZE * y + Settings.CELL_SIZE / 2)
                if pygame.sprite.collide_mask(
                        self, list(Settings.BACKGROUND_MAP)[0]):
                    Settings.BOARD[y][x] = 'X'
        # for i in Settings.BOARD:
        #     print(*i)
        # print()

        self.kill()
