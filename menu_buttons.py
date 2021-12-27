from Settings import *


class Title(pygame.sprite.Sprite):
    """Класс с названием игры"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = TITLE_IMAGE
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, HEIGHT // 5

    def update(self, pos):
        # сюда можно впихнуть пасхалку
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class NewGame(pygame.sprite.Sprite):
    """Класс с кнопкой начала новой игры"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = NEW_CAMPAIGN_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.game_screen = True


class Load(pygame.sprite.Sprite):
    """Класс с кнопкой загрузки сохранения"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = LOAD_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 400
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class Settings(pygame.sprite.Sprite):
    """Класс с кнопкой настроек"""
    def __init__(self, run):
        pygame.sprite.Sprite.__init__(self)
        img = SETTINGS_BUTTON
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = WIDTH // 2, 500

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


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
