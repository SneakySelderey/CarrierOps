import pygame


# Класс, ответственный за отрисовку квадратов
class Board:
    def __init__(self, width, height, run):
        self.run = run
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    # метод, задающий отступ сетки и размер одного квадрата
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.run.cell_size = cell_size

    # метод, отрисовывающий сетку
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('darkred'),
                                 (x * self.run.cell_size + self.left, y * self.run.cell_size + self.top,
                                  self.run.cell_size, self.run.cell_size), 1)