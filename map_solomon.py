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