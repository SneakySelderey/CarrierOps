import pygame
from Settings import BASE_FRIENDLY, BASE_HOSTILE, BASE_NEUTRAL, \
    random_resource_type, OIL_ICON, \
    GEAR_ICON, PLANE_ICON, MISSILE_ICON, \
    PLAYER_BASE, AI_BASE, BASES_SPRITES, ALL_SPRITES_FOR_SURE, ALWAYS_UPDATE
import Settings
from math import hypot


class Base(pygame.sprite.Sprite):
    """Класс, определяющий спрайт и местоположение базы-острова"""
    Images = {'friendly': BASE_FRIENDLY, 'neutral': BASE_NEUTRAL,
              'hostile': BASE_HOSTILE, 'player': PLAYER_BASE, 'ai': AI_BASE}
    ResourceType = {'oil': OIL_ICON, 'repair': GEAR_ICON,
                    'missile': MISSILE_ICON, 'aircraft': PLANE_ICON}

    def __init__(self, x, y, state, visibility):
        super().__init__(ALL_SPRITES_FOR_SURE, BASES_SPRITES,
                         ALWAYS_UPDATE)
        self.x, self.y = x, y
        self.image = pygame.transform.scale(Base.Images[state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.state = state
        self.to_add = True
        self.rect = self.image.get_rect(topleft=[
            x * Settings.CELL_SIZE + Settings.LEFT,
            y * Settings.CELL_SIZE + Settings.TOP])
        self.visibility = visibility
        self.ticks_to_capture = Settings.BASE_TICKS
        self.start_of_capture = 0
        self.prev_start = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.show_bar = False
        if self.state not in ['player', 'ai']:
            self.resource_type = random_resource_type()
            self.ticks_to_give_resource = 0

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
                self.state = 'friendly'
                Settings.BASES_CAPT_PLAYER += 1
                if base_grid in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.remove(base_grid)
                if base_grid not in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.append(base_grid)
            elif self.start_of_capture == 2:
                self.state = 'hostile'
                Settings.BASES_CAPT_AI += 1
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)

            self.image = pygame.transform.scale(Base.Images[self.state], (
                Settings.CELL_SIZE, Settings.CELL_SIZE))
            if self.state == 'friendly':
                for ai in list(Settings.AI_SPRITE):
                    if hypot(ai.rect.centerx - self.rect.centerx,
                             ai.rect.centery - self.rect.centery) <= \
                            Settings.CELL_SIZE * 15:
                        ai.missile_launch(self.rect.center)

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + Settings.LEFT,
                             self.y * Settings.CELL_SIZE + Settings.TOP]

        if self.ticks_to_give_resource and not Settings.IS_PAUSE:
            self.ticks_to_give_resource -= 1
        elif not Settings.IS_PAUSE:
            state = 'player' if self.state == 'friendly' else 'ai'
            main_bases = [base for base in Settings.BASES_SPRITES if
                          base.state == state]
            self.ticks_to_give_resource = Settings.GIVE_RESOURCE_TIME
            if self.resource_type == 'oil':
                for base in main_bases:
                    base.oil_volume = min(base.oil_volume + 1, 100)
            elif self.resource_type == 'missile':
                for base in main_bases:
                    base.num_of_missiles += 1
            elif self.resource_type == 'aircraft':
                for base in main_bases:
                    base.num_of_aircraft += 1
            else:
                for base in main_bases:
                    base.num_of_repair_parts += 1

    def new_position(self, cell, top, left):
        """Функция для подсчета новых координат после изменения разрешения"""
        self.image = pygame.transform.scale(Base.Images[self.state], (
            Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect(topleft=[self.x * cell + left,
                                                 self.y * cell + top])
        self.mask = pygame.mask.from_surface(self.image)

    def data_to_save(self):
        """Функуия, возвращающая список значений, которые можно сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['image'], to_save['mask']
        return 'base', to_save


class SuperBase(Base):
    """Класс для галвнйо базы"""
    def __init__(self, *args):
        super().__init__(*args)
        self.ticks_to_capture = 0
        self.num_of_aircraft = self.num_of_missiles = self.oil_volume = \
            self.num_of_repair_parts = 0
        if self.state == 'ai':
            Settings.HOSTILE_BASES.append((self.x, self.y))
            self.start_of_capture = 2
            self.visibility = True
        else:
            self.start_of_capture = 1
            Settings.FRIENDLY_BASES.append((self.x, self.y))

    def update(self):
        """Обновление изображения базы, если она захватывается"""
        base_grid = self.x, self.y
        prev_start = self.start_of_capture
        player = list(Settings.PLAYER_SPRITE)[0]
        if pygame.sprite.collide_mask(self, player) and not Settings.IS_PAUSE:
            self.start_of_capture = 1
            if self.state == 'player':
                self.give_resources(player)
        for ai in Settings.AI_SPRITE:
            if pygame.sprite.collide_mask(self, ai) and not \
                    pygame.sprite.collide_mask(self, player):
                self.start_of_capture = 2
                if self.state == 'ai':
                    self.give_resources(ai)

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
                Settings.BASES_CAPT_PLAYER += 1
                if base_grid in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.remove(base_grid)
                    for ai in list(Settings.AI_SPRITE):
                        if hypot(ai.rect.centerx - self.rect.centerx,
                                 ai.rect.centery - self.rect.centery) <= \
                                Settings.CELL_SIZE * 15:
                            ai.missile_launch(self.rect.center)
                if base_grid not in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.append(base_grid)
            elif self.start_of_capture == 2:
                self.state = 'ai'
                Settings.BASES_CAPT_AI += 1
                if base_grid in Settings.FRIENDLY_BASES:
                    Settings.FRIENDLY_BASES.remove(base_grid)
                if base_grid not in Settings.HOSTILE_BASES:
                    Settings.HOSTILE_BASES.append(base_grid)

            self.image = pygame.transform.scale(Base.Images[self.state], (
                Settings.CELL_SIZE, Settings.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x * Settings.CELL_SIZE + Settings.LEFT,
                             self.y * Settings.CELL_SIZE + Settings.TOP]

    def data_to_save(self):
        """Функуия, возвращающая список значений, которые можно сохранить"""
        to_save = self.__dict__.copy()
        del to_save['_Sprite__g'], to_save['image'], to_save['mask']
        return 'super base', to_save

    def give_resources(self, obj):
        """Функция для пополнения запасов ресурсов на авианосце"""
        obj.num_of_aircraft += self.num_of_aircraft
        obj.num_of_missiles += self.num_of_missiles
        oil_lack = min(100 - obj.oil_volume, self.oil_volume)
        self.oil_volume -= oil_lack
        obj.oil_volume += oil_lack
        hp_lack = min((100 - obj.current_health) // 10,
                      self.num_of_repair_parts)
        self.num_of_repair_parts -= hp_lack
        obj.current_health += hp_lack * 10
        self.num_of_aircraft = 0
        self.num_of_missiles = 0
