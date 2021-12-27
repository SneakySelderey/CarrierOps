from Settings import *


class MainMenu(pygame.sprite.Sprite):
    """Класс с кнопкой, ведущей в главное меню"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = MAIN_MENU_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, HEIGHT)
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            for sound in ALL_SOUNDS:
                sound.stop()
                self.run.__init__()
