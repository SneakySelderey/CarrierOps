import pygame
from Settings import BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, ALL_SPRITES, \
    BASES_SPRITES, ALL_SPRITES_FOR_SURE, random_resource_type, OIL_ICON, \
    GEAR_ICON, PLANE_ICON, MISSILE_ICON, new_image_size, BLUE, RED, \
    PLAYER_BASE, AI_BASE
import Settings


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE, 'player': PLAYER_BASE, 'ai': AI_BASE}
    ResourceType = {'oil': [OIL_ICON, Settings.OIL_VOLUME],
                    'repair': [GEAR_ICON, Settings.NUM_OF_REPAIR_PARTS],
                    'missile': [MISSILE_ICON, Settings.NUM_OF_MISSILES],
                    'aircraft': [PLANE_ICON, Settings.NUM_OF_AIRCRAFT]}

    def __init__(self, x, y, state, visibility, cell_size, parent):
        super().__init__(ALL_SPRITES, BASES_SPRITES, ALL_SPRITES_FOR_SURE)
        self.x, self.y = x, y
        self.size = cell_size
        self.parent = parent
        self.image = pygame.transform.scale(Base.Images[state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.state = state
        self.to_add = True
        self.rect = self.image.get_rect()
        self.rect.topleft = [x * cell_size + parent.left,
                             y * cell_size + parent.top]
        self.visibility = visibility
        self.ticks_to_capture = Settings.BASE_TICKS
        self.start_of_capture = 0
        self.mask = pygame.mask.from_surface(self.image)
        if self.state == 'ai':
            Settings.HOSTILE_BASES.append(self)
            self.visibility = False
        elif self.state == 'player':
            Settings.FRIENDLY_BASES.append(self)
        self.ticks_to_give_resource = None
        if self.state not in ['player', 'ai']:
            self.resource_type = random_resource_type()
            self.ico = BaseIcon(self)
            self.bar = BaseBar(self)
            self.ticks_to_give_resource = Settings.GIVE_RESOURCE_TIME

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        prev_start = self.start_of_capture
        player = list(Settings.PLAYER_SPRITE)[0]
        if pygame.sprite.collide_mask(self, player) and self.state != 'player':
            self.start_of_capture = 1
        if self.state != 'ai':
            for ai in Settings.AI_SPRITE:
                if pygame.sprite.collide_mask(self, ai) and not \
                        pygame.sprite.collide_mask(self, player):
                    self.start_of_capture = 2

        self.ticks_to_capture = self.ticks_to_capture if \
            prev_start == self.start_of_capture else Settings.BASE_TICKS

        if prev_start != self.start_of_capture:
            self.to_add = True

        if self.ticks_to_capture and self.start_of_capture:
            self.ticks_to_capture -= 1
        elif self.to_add:
            self.to_add = False
            if self.start_of_capture == 1:
                self.state = 'friendly' if self.state != 'ai' else 'player'
                if base_grid in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.remove(base_grid)
                if base_grid not in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.append(base_grid)
            elif self.start_of_capture == 2:
                self.state = 'hostile' if self.state != 'player' else 'ai'
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)

            self.image = pygame.transform.scale(Base.Images[self.state], (
                Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + self.parent.left,
                             self.y * Settings.CELL_SIZE + self.parent.top]

        if self.state not in ['player', 'ai'] and self.ticks_to_give_resource \
                is not None:
            if self.ticks_to_give_resource:
                self.ticks_to_give_resource -= 1
            elif self.state == 'friendly':
                self.ticks_to_give_resource = Settings.GIVE_RESOURCE_TIME
                if self.resource_type == 'oil':
                    Settings.BASE_OIL_VOLUME = min(
                        Settings.BASE_OIL_VOLUME + 1, 100)
                elif self.resource_type == 'missile':
                    Settings.BASE_NUM_OF_MISSILES += 1
                elif self.resource_type == 'aircraft':
                    Settings.BASE_NUM_OF_AIRCRAFT += 1
                else:
                    Settings.BASE_NUM_OF_REPAIR_PARTS += 1

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
        self.image = new_image_size(Base.ResourceType[self.resource][0])
        self.rect = self.image.get_rect(bottomleft=base.rect.topright)
        self.parent = base
        self.visibility = True

    def update(self):
        """Обновления положения"""
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)

    def new_position(self):
        """обновление положеняи при изменении разрешения"""
        self.image = new_image_size(Base.ResourceType[self.resource][0])
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)


class BaseBar(pygame.sprite.Sprite):
    """Класс для полоски захвата базы"""
    def __init__(self, base):
        """Инициализация. Принимает базу"""
        super().__init__(ALL_SPRITES_FOR_SURE, ALL_SPRITES)
        self.parent = base
        self.image = pygame.Surface((Settings.CELL_SIZE, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=(base.rect.topleft[0],
                                                    base.rect.topleft[1] - 10))
        self.visibility = True

    def update(self):
        """Обновление полоски"""
        if self.parent.start_of_capture and self.parent.ticks_to_capture:
            self.image = pygame.Surface((int(
                Settings.CELL_SIZE - Settings.CELL_SIZE / Settings.BASE_TICKS
                * self.parent.ticks_to_capture), 5))
            self.image.fill(BLUE if self.parent.start_of_capture == 1 else RED)
        else:
            self.image = self.image = pygame.Surface((Settings.CELL_SIZE, 10),
                                                     pygame.SRCALPHA)
        self.rect.bottomleft = (self.parent.rect.topleft[0],
                                self.parent.rect.topleft[1] - 10)

    def new_position(self):
        """Обновление позиции при изменении разрешения"""
        self.image = pygame.Surface((Settings.CELL_SIZE, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=(
            self.parent.rect.topleft[0], self.parent.rect.topleft[1] - 10))
