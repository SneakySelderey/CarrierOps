from Settings import *


class BasesLost(pygame.sprite.Sprite):
    """Класс с надписью о том, что все базы захвачены противником"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = BASES_LOST_IMAGE
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class MainMenu(pygame.sprite.Sprite):
    """Класс с кнопкой, ведущей в главное меню"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = MAIN_MENU_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 500
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.main()


class Quit(pygame.sprite.Sprite):
    """Класс с кнопкой выхода из игры"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = QUIT_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 600
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.running = False
