import pygame
from Settings import DARK_RED


class Board:
    """Класс, ответственный за отрисовку поля"""
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        """Метод, задающий отступ сетки и размер одной ячейки"""
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        """Метод, отрисовывающий сетку"""
        [pygame.draw.rect(screen, DARK_RED, (
            x * self.cell_size + self.left,
            y * self.cell_size + self.top, self.cell_size,
            self.cell_size), 1) for y in range(self.height)
         for x in range(self.width)]