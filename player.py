import pygame


# класс, определяющий параметеры и спрайт игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, visibility):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load('data/img/Player_cursor.png').convert()
        self.image = player_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [25, 25]
        self.speedx = 0
        self.speedy = 0

        self.visibility = visibility

    # обновление позиции спрайта
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy