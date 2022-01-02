import pygame
from Settings import BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, ALL_SPRITES
import Settings


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE}

    def __init__(self, x, y, state, visibility, cell_size):
        super().__init__(ALL_SPRITES)
        self.x, self.y = x, y
        self.size = cell_size
        self.image = pygame.transform.scale(Base.Images[state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.state = state
        self.rect = self.image.get_rect()
        self.rect.topleft = [x * cell_size, y * cell_size]
        self.visibility = visibility

        Settings.BASES_SPRITES.add(self)
        Settings.ALL_SPRITES_FOR_SURE.add(self)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        for player in Settings.PLAYER_SPRITE:
            if pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(Base.Images['friendly'], (Settings.CELL_SIZE, Settings.CELL_SIZE))
                if base_grid in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.remove(base_grid)
                if base_grid not in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.append(base_grid)
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_mask(self, ai) and not pygame.sprite.collide_mask(self, player):
                self.image = pygame.transform.scale(Base.Images['hostile'], (Settings.CELL_SIZE, Settings.CELL_SIZE))
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.rect.topleft = [self.x * self.size, self.y * self.size]
        self.image = pygame.transform.scale(Base.Images[self.state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
