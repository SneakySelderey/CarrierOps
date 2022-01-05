import pygame
import Settings
from base import Base, SuperBase
from random import sample, randint, choice


class Board:
    """Класс, ответственный за отрисовку поля"""
    def __init__(self, width, height):
        self.cell_size = Settings.CELL_SIZE
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
        self.bases = []
        self.left = 20
        self.top = 20
        self.cell_size = 30
        self.cells = [(i, j) for i in range(self.width) for j in
                      range(self.height)]

    def set_view(self, left, top, cell_size):
        """Метод, задающий отступ сетки и размер одной ячейки"""
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def add_bases(self):
        """Функция для добавления баз"""
        player_base, *bases, ai_base = sorted(sample(
            self.cells, Settings.NUM_OF_BASES + 2))
        Settings.PLAYER_START = player_base
        Settings.AI_START = ai_base
        [self.add_base(*base) for base in bases]
        self.add_base(player_base[0], player_base[1], 'player')
        self.add_base(ai_base[0], ai_base[1], 'ai')

    def add_base(self, x, y, *mega):
        """Функция для добавления базы на поле"""
        if not mega:
            base = Base(x, y, 'neutral', True, self.cell_size, self)
        else:
            base = SuperBase(x, y, mega[0], True, self.cell_size, self)
        land = list(Settings.BACKGROUND_MAP)[0]
        while land.rect.collidepoint(x, y) and land.mask.get_at(
                (x - land.rect.x, y - land.rect.y)):
            a, b = choice(self.cells)
            base.rect.center = a * Settings.CELL_SIZE, b * Settings.CELL_SIZE
        try:
            self.cells.remove((a, b))
        except NameError:
            pass
        self.board[x][y] = base
        self.bases.append(base)

    def render(self, screen):
        """Метод, отрисовывающий сетку"""
        self.cell_size = Settings.CELL_SIZE
        [pygame.draw.rect(screen, Settings.GREY, (
            x * self.cell_size + self.left,
            y * self.cell_size + self.top, self.cell_size,
            self.cell_size), 1) for y in range(self.height)
         for x in range(self.width)]

    def update(self):
        """Обновление размера сетки"""
        self.cell_size = Settings.CELL_SIZE

    def get_cell(self, mouse_pos):
        """Функция для определения ячейки, на которую нажал пользователь"""
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if not 0 <= x <= self.width or not 0 <= y <= self.height:
            return
        return x, y

    def on_click(self, cell_pos):
        """Функция"""
        x, y = cell_pos  # TODO: WHEN PRESSING ON BOARD

    def get_click(self, mouse_pos):
        """Функия для полчения клика на поле. Если пользователь нажал на поле,
         идет обработка этого события"""
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)