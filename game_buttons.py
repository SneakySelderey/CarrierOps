from Settings import *
import pygame


class MainMenu(pygame.sprite.Sprite):
    """Класс с кнопкой, ведущей в главное меню"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('MAIN MENU', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.bottomleft = (0, HEIGHT)
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            for sound in ALL_SOUNDS:
                sound.stop()
            self.run.__init__()
