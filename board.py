import pygame
import Settings
from base import Base, SuperBase
from random import sample, choice


class Board:
    """Класс, ответственный за отрисовку поля"""
    def __init__(self, width, height, run):
        self.cell_size = Settings.CELL_SIZE
        self.width = width
        self.height = height
        self.bases = []
        self.left = 20
        self.top = 20
        self.cell_size = 30
        Settings.TOP, Settings.LEFT = self.top, self.left
        self.cells = {(i, j) for i in range(self.width) for j in
                      range(self.height)}
        self.used = set()
        self.run = run

    def set_view(self, left, top, cell_size):
        """Метод, задающий отступ сетки и размер одной ячейки"""
        self.left = left
        self.top = top
        self.cell_size = cell_size
        Settings.TOP, Settings.LEFT = top, left

    def add_bases(self):
        """Функция для добавления баз"""
        self.cell_size = Settings.CELL_SIZE
        player_base, *bases, ai_base = sorted(sample(
            self.cells, Settings.NUM_OF_BASES + 2))
        [self.add_base(*base) for base in bases]
        self.add_base(player_base[0], player_base[1], 'player')
        self.add_base(ai_base[0], ai_base[1], 'ai')

    def add_base(self, x, y, *mega):
        """Функция для добавления базы на поле"""
        if not mega:
            base = Base(x, y, 'neutral', True)
        else:
            base = SuperBase(x, y, mega[0], True)
        land = list(Settings.BACKGROUND_MAP)[0]
        while pygame.sprite.collide_mask(land, base) is not None:
            self.used.add((x, y))
            x, y = choice(list(self.cells - self.used))
            base.x, base.y = x, y
            base.new_position(self.cell_size, self.top, self.left)
        self.used.add((x, y))
        if mega and mega[0] == 'player':
            Settings.PLAYER_START = (x, y)
        elif mega and mega[0] == 'ai':
            Settings.AI_START = (x, y)
        self.bases.append(base)

    def render(self, screen):
        """Метод, отрисовывающий сетку"""
        self.cell_size = Settings.CELL_SIZE
        [pygame.draw.rect(screen, Settings.GREY, (
            x * self.cell_size + self.left,
            y * self.cell_size + self.top, self.cell_size,
            self.cell_size), 1) for y in range(self.height)
         for x in range(self.width)]

    def get_cell(self, mouse_pos):
        """Функция для определения ячейки, на которую нажал пользователь"""
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if not 0 <= x <= self.width or not 0 <= y <= self.height:
            return
        return x, y