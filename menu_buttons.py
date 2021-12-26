import pygame


class Title(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/title.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, size[1] // 5

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class NewGame(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/new_campaign.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.menu_screen = False
            self.run.game_screen = True


class Load(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/load.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 400
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class Settings(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/settings.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = size[0] // 2, 500

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


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

