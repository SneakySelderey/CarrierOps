import pygame


# класс, определяющий спрайт и местоположение базы-острова
class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, state, visibility, cell_size):
        pygame.sprite.Sprite.__init__(self)
        if state == 'neutral':
            base_img = pygame.image.load('data/img/base_neutral.png').convert()
        elif state == 'friendly':
            base_img = pygame.image.load('data/img/base_friendly.png').convert()
        elif state == 'hostile':
            base_img = pygame.image.load('data/img/base_hostile.png').convert()
        self.image = base_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [x + cell_size // 2, y + cell_size // 2]

        self.visibility = visibility
