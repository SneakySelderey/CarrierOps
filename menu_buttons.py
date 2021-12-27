from Settings import *
import pygame


class Title(pygame.sprite.Sprite):
    """Класс с названием игры"""
    def __init__(self):
        super().__init__()
        txt = MAIN_FONT.render('CARRIER OPERATIONS', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, HEIGHT // 5

    def update(self, pos):
        # сюда можно впихнуть пасхалку
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class NewGame(pygame.sprite.Sprite):
    """Класс с кнопкой начала новой игры"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('NEW CAMPAIGN', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.game_screen = True


class Load(pygame.sprite.Sprite):
    """Класс с кнопкой загрузки сохранения"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('LOAD SAVE', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, 400
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class Settings(pygame.sprite.Sprite):
    """Класс с кнопкой настроек"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('SETTINGS', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.center = WIDTH // 2, 500

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class Quit(pygame.sprite.Sprite):
    """Класс с кнопкой выхода из игры"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('QUIT TO DESKTOP', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, 600
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.running = False
