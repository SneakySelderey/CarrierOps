import pygame


class MainMenu(pygame.sprite.Sprite):
    def __init__(self, size, run):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/img/main_menu.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, size[1])
        self.run = run

    def update(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.run.main()
