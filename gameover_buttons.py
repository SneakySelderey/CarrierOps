from Settings import *


class BasesLost(pygame.sprite.Sprite):
    """Класс с надписью о том, что все базы захвачены противником"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render("GAME OVER. YOU'VE LOST ALL BASES.", True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, 300
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            pass


class MainMenu(pygame.sprite.Sprite):
    """Класс с кнопкой, ведущей в главное меню"""
    def __init__(self, run):
        super().__init__()
        txt = MAIN_FONT.render('MAIN MENU', True, WHITE)
        self.image = pygame.Surface(txt.get_size(), pygame.SRCALPHA, 32)
        self.rect = txt.get_rect()
        self.image.blit(txt, self.rect)
        self.rect.centerx, self.rect.centery = WIDTH // 2, 500
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.__init__()


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
