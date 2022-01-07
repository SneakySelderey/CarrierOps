import pygame
from Settings import BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, ALL_SPRITES, \
    BASES_SPRITES, ALL_SPRITES_FOR_SURE, random_resource_type, OIL_ICON, \
    GEAR_ICON, PLANE_ICON, MISSILE_ICON, new_image_size, BLUE, RED, \
    PLAYER_BASE, AI_BASE, BASES_SPRITES, ALL_SPRITES_FOR_SURE, ALWAYS_UPDATE
import Settings


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE, 'player': PLAYER_BASE, 'ai': AI_BASE}
    ResourceType = {'oil': [OIL_ICON, Settings.OIL_VOLUME],
                    'repair': [GEAR_ICON, Settings.NUM_OF_REPAIR_PARTS],
                    'missile': [MISSILE_ICON, Settings.NUM_OF_MISSILES],
                    'aircraft': [PLANE_ICON, Settings.NUM_OF_AIRCRAFT]}

    def __init__(self, x, y, state, visibility, cell_size, parent, run):
        super().__init__(ALL_SPRITES_FOR_SURE, ALL_SPRITES, BASES_SPRITES,
                         ALWAYS_UPDATE)
        self.x, self.y = x, y
        self.size = cell_size
        self.parent = parent
        self.image = pygame.transform.scale(Base.Images[state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.state = state
        self.to_add = True
        self.rect = self.image.get_rect(center=[
            x * cell_size + parent.left + cell_size // 2,
            y * cell_size + parent.top + cell_size // 2])
        self.visibility = visibility
        self.ticks_to_capture = Settings.BASE_TICKS
        self.start_of_capture = 0
        self.prev_start = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.bar = BaseBar(self)
        if self.state not in ['player', 'ai']:
            self.resource_type = random_resource_type()
            self.ico = BaseIcon(self)
            self.ticks_to_give_resource = Settings.GIVE_RESOURCE_TIME
        self.run = run

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        self.prev_start = self.start_of_capture
        player = list(Settings.PLAYER_SPRITE)[0]
        if pygame.sprite.collide_mask(self, player):
            self.start_of_capture = 1
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_mask(self, ai) and not \
                    pygame.sprite.collide_mask(self, player):
                self.start_of_capture = 2

        self.ticks_to_capture = self.ticks_to_capture if \
            self.prev_start == self.start_of_capture else Settings.BASE_TICKS

        if self.prev_start != self.start_of_capture:
            self.to_add = True

        if self.ticks_to_capture and self.start_of_capture and not \
                Settings.IS_PAUSE:
            self.ticks_to_capture -= 1
        elif self.to_add and not Settings.IS_PAUSE:
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
            if self.state == 'friendly':
                self.run.bases_captured_by_player += 1
            elif self.state == 'hostile':
                self.run.bases_captured_by_AI += 1

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + self.parent.left,
                             self.y * Settings.CELL_SIZE + self.parent.top]

        if self.ticks_to_give_resource and not Settings.IS_PAUSE:
            self.ticks_to_give_resource -= 1
        elif self.state == 'friendly' and not Settings.IS_PAUSE:
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

    def new_position(self, cell, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.rect.topleft = [self.x * cell + left,
                             self.y * cell + top]
        self.image = pygame.transform.scale(Base.Images[self.state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.mask = pygame.mask.from_surface(self.image)


class SuperBase(Base):
    """Класс для галвнйо базы"""
    def __init__(self, *args, run):
        super().__init__(*args, run)
        self.ticks_to_capture = Settings.BASE_TICKS
        if self.state == 'ai':
            Settings.HOSTILE_BASES.append((self.x, self.y))
            self.start_of_capture = 2
            self.visibility = False
        else:
            self.start_of_capture = 1
            Settings.FRIENDLY_BASES.append((self.x, self.y))

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        prev_start = self.start_of_capture
        player = list(Settings.PLAYER_SPRITE)[0]
        if pygame.sprite.collide_mask(self, player):
            self.start_of_capture = 1
            if self.state == 'player':
                Settings.NUM_OF_AIRCRAFT += Settings.BASE_NUM_OF_AIRCRAFT
                Settings.NUM_OF_MISSILES += Settings.BASE_NUM_OF_MISSILES
                oil_lack = min(100 - Settings.OIL_VOLUME, Settings.BASE_OIL_VOLUME)
                Settings.BASE_OIL_VOLUME -= oil_lack
                Settings.OIL_VOLUME += oil_lack
                Settings.OIL_VOLUME += Settings.BASE_OIL_VOLUME
                hp_lack = min((100 - player.current_health) // 10,
                              Settings.BASE_NUM_OF_REPAIR_PARTS)
                Settings.BASE_NUM_OF_REPAIR_PARTS -= hp_lack
                player.current_health += hp_lack * 10
                Settings.BASE_NUM_OF_AIRCRAFT = 0
                Settings.BASE_NUM_OF_MISSILES = 0
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_mask(self, ai) and not \
                    pygame.sprite.collide_mask(self, player):
                self.start_of_capture = 2

        self.ticks_to_capture = self.ticks_to_capture if \
            prev_start == self.start_of_capture else Settings.BASE_TICKS

        if prev_start != self.start_of_capture:
            self.to_add = True

        if self.ticks_to_capture and self.start_of_capture and not \
                Settings.IS_PAUSE:
            self.ticks_to_capture -= 1
        elif self.to_add and not Settings.IS_PAUSE:
            self.to_add = False
            if self.start_of_capture == 1:
                self.state = 'player'
                if base_grid in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.remove(base_grid)
                if base_grid not in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.append(base_grid)
            elif self.start_of_capture == 2:
                self.state = 'ai'
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)

            self.image = pygame.transform.scale(Base.Images[self.state], (
                Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + self.parent.left,
                             self.y * Settings.CELL_SIZE + self.parent.top]


class BaseIcon(pygame.sprite.Sprite):
    """Класс для иконки ресурса рядом с базой"""
    def __init__(self, base):
        """Инициализация. Принимает базу"""
        super().__init__(ALL_SPRITES, ALL_SPRITES_FOR_SURE, ALWAYS_UPDATE)
        self.resource = base.resource_type
        self.image = new_image_size(Base.ResourceType[self.resource][0])
        self.rect = self.image.get_rect(bottomleft=base.rect.topright)
        self.parent = base
        self.visibility = True

    def update(self):
        """Обновления положения"""
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)

    def new_position(self, cell, top, left):
        """обновление положеняи при изменении разрешения"""
        self.image = new_image_size(Base.ResourceType[self.resource][0])
        self.rect = self.image.get_rect(bottomleft=self.parent.rect.topright)


class BaseBar(pygame.sprite.Sprite):
    """Класс для полоски захвата базы"""
    def __init__(self, base):
        """Инициализация. Принимает базу"""
        super().__init__(ALL_SPRITES_FOR_SURE, ALL_SPRITES, ALWAYS_UPDATE)
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
            self.image = pygame.Surface((Settings.CELL_SIZE, 10),
                                        pygame.SRCALPHA)
        self.rect.bottomleft = (self.parent.rect.topleft[0],
                                self.parent.rect.topleft[1] - 10)

    def new_position(self, cell, top, left):
        """Обновление позиции при изменении разрешения"""
        self.image = pygame.Surface((Settings.CELL_SIZE, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=(
            self.parent.rect.topleft[0], self.parent.rect.topleft[1] - 10))
