import pygame


# класс, определяющий параметры и спрайт ИИ
class AI(pygame.sprite.Sprite):
    def __init__(self, board, visibility, cell_size):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load('data/img/AI_cursor.png').convert()
        self.image = player_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [cell_size * board.width, cell_size * board.height]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

    # обновление позиции спрайта
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy