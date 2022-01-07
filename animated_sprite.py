import pygame
import Settings
from Settings import new_image_size


class AnimatedSprite(pygame.sprite.Sprite):
    """Класс для анимированного спрайта"""
    def __init__(self, sheet, columns, rows, *groups):
        """Инициализация. Принимает картинку, кличество столбцов и строк и
        группы спарйтов, где должен быть объект"""
        super().__init__(Settings.ALL_SPRITES_FOR_SURE,
                         Settings.ANIMATED_SPRTIES, *groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = new_image_size(self.frames[self.cur_frame])

    def cut_sheet(self, sheet, columns, rows):
        """Функция для создания отдельных кадрос из листа"""
        self.cur_frame = 0
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        self.frames = [sheet.subsurface(pygame.Rect(
            (self.rect.w * i, self.rect.h * j), self.rect.size)) for j in
            range(rows) for i in range(columns)]

    def update_frame(self):
        """Установка нового кадра"""
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = new_image_size(self.frames[self.cur_frame])