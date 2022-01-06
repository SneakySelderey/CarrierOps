import pygame
import Settings
from Settings import new_image_size


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, *groups):
        super().__init__(Settings.ALL_SPRITES_FOR_SURE, Settings.ALL_SPRITES,
                         Settings.ANIMATED_SPRTIES, *groups)
        self.frames = []
        self.cut_sheet(new_image_size(sheet), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_frame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]