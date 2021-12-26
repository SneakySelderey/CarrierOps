import pygame


class BasesLost(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/all_bases_lost.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class MainMenu(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/main_menu.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 500
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = True
            self.run.gameover_screen = False


class Quit(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/quit.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 600
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.running = False
