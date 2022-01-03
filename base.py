import pygame
from Settings import BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, ALL_SPRITES, \
    BASES_SPRITES, ALL_SPRITES_FOR_SURE, random_resource_type, OIL_ICON, \
    GEAR_ICON, PLANE_ICON, MISSILE_ICON, new_image_size, new_coords
import Settings


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE}
    ResourceType = {'oil': OIL_ICON, 'repair': GEAR_ICON,
                    'missile': MISSILE_ICON, 'aircraft': PLANE_ICON}

    def __init__(self, x, y, state, visibility, cell_size, parent):
        super().__init__(ALL_SPRITES, BASES_SPRITES, ALL_SPRITES_FOR_SURE)
        self.x, self.y = x, y
        self.size = cell_size
        self.parent = parent
        self.image = pygame.transform.scale(Base.Images[state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.state = state
        self.rect = self.image.get_rect()
        self.rect.topleft = [x * cell_size + parent.left,
                             y * cell_size + parent.top]
        self.resource_type = random_resource_type()
        self.visibility = visibility
        self.mask = pygame.mask.from_surface(self.image)
        self.ico = BaseIcon(self)

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        player = list(Settings.PLAYER_SPRITE)[0]
        if pygame.sprite.collide_mask(self, player):
            self.state = 'friendly'
            if base_grid in Settings.HOSTILE_BASES:
                Settings.HOSTILE_BASES.remove(base_grid)
            if base_grid not in Settings.FRIENDLY_BASES:
                Settings.FRIENDLY_BASES.append(base_grid)
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_mask(self, ai) and not \
                    pygame.sprite.collide_mask(self, player):
                self.state = 'hostile'
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)
        self.image = pygame.transform.scale(Base.Images[self.state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + self.parent.left,
                             self.y * Settings.CELL_SIZE + self.parent.top]

    def new_position(self):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.rect.topleft = [self.x * self.size, self.y * self.size]
        self.image = pygame.transform.scale(Base.Images[self.state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.mask = pygame.mask.from_surface(self.image)


class BaseIcon(pygame.sprite.Sprite):
    """Класс для иконки ресурса рядом с базой"""
    def __init__(self, base):
        """Инициализация. Принимает базу"""
        super().__init__(ALL_SPRITES, ALL_SPRITES_FOR_SURE)
        self.resource = base.resource_type
        self.image = new_image_size(Base.ResourceType[self.resource])
        self.rect = self.image.get_rect(bottomleft=base.rect.topright)
        self.parent = base
        self.visibility = True

    def update(self):
        """Обновления положения"""
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)

    def new_position(self):
        """обновление положеняи при изменении разрешения"""
        self.image = new_image_size(Base.ResourceType[self.resource])
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)

