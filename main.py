import pygame
import random
from math import sqrt


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        Run.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('darkred'),
                                 (x * Run.cell_size + self.left, y * Run.cell_size + self.top,
                                  Run.cell_size, Run.cell_size), 1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load('img/Player_cursor.png').convert()
        self.image = player_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [25, 25]
        self.speedx = 0
        self.speedy = 0
        self.missiles = 5

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class AI(pygame.sprite.Sprite):
    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load('img/AI_cursor.png').convert()
        self.image = player_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [Run.cell_size * board.width, Run.cell_size * board.height]
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, state):
        pygame.sprite.Sprite.__init__(self)
        if state == 'neutral':
            base_img = pygame.image.load('img/base_neutral.png').convert()
        elif state == 'friendly':
            base_img = pygame.image.load('img/base_friendly.png').convert()
        elif state == 'hostile':
            base_img = pygame.image.load('img/base_hostile.png').convert()
        self.image = base_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [x + Run.cell_size // 2, y + Run.cell_size // 2]


class MissileFriendly(pygame.sprite.Sprite):
    def __init__(self, player, first_pos_check, activation):
        pygame.sprite.Sprite.__init__(self)
        base_img = pygame.image.load('img/missile_friendly.png').convert()
        self.image = base_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        if first_pos_check:
            self.rect.center = [player.rect.centerx, player.rect.centery]
            first_pos_check = False
            self.pos = pygame.math.Vector2([player.rect.centerx, player.rect.centery])
            self.dir = pygame.math.Vector2((activation[0] - player.rect.centerx,
                                            activation[1] - player.rect.centery)).normalize()

        self.activated = False
        self.turn_one_side = True
        self.turn_another_side = False
        self.first_rotate = True

        self.activation = activation

        self.ticks = 10
        self.speed = 50
        self.total_ticks = 0

        self.ticks1 = 0
        self.speed1 = 50

    def update(self):
        clock = pygame.time.Clock()
        clock1 = pygame.time.Clock()

        if not self.activated:
            if self.ticks1 >= self.speed1:
                self.total_ticks += 1
                self.ticks1 = 0
            clock1.tick(300)
            self.ticks1 += 1

        if self.pos != self.activation:
            self.pos += self.dir * 2
            x = int(self.pos.x)
            y = int(self.pos.y)
            self.rect.center = x, y

        if self.activation[0] - 10 < round(self.pos.x) < self.activation[0] + 10 \
                and self.activation[1] - 10 < round(self.pos.y) < self.activation[1] + 10:
            self.activated = True

        if self.activated:
            if self.ticks >= self.speed:
                self.total_ticks += 1
                self.ticks = 0
                if self.first_rotate:
                    self.dir = self.dir.rotate(-40)
                    self.first_rotate = False
                elif self.turn_one_side:
                    self.dir = self.dir.rotate(80)
                    self.first_rotate = False
                    self.turn_one_side = False
                    self.turn_another_side = True
                elif self.turn_another_side:
                    self.dir = self.dir.rotate(-80)
                    self.turn_one_side = True
                    self.turn_another_side = False
            clock.tick(300)
            self.ticks += 1


class Run:
    def __init__(self):
        pass

    def missile_launch(self, destination, player, bases):
        self.friendly_missiles.append(MissileFriendly(player, True, destination))
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(player, bases, self.friendly_missiles)

        self.sound_fire_VLS.play()

    def friendly_missile_movement(self, screen, missile):
        for missile in self.friendly_missiles:
            pygame.draw.line(screen, pygame.Color('blue'), (missile.rect.centerx, missile.rect.centery),
                             (missile.activation[0], missile.activation[1]))
            pygame.draw.circle(screen, pygame.Color('blue'), (missile.rect.centerx, missile.rect.centery), 100, 1)

            if missile.total_ticks == 10:
                self.friendly_missiles.remove(missile)

    def movement_player(self, destination, player, screen):
        stop_x, stop_y = False, False
        if destination[0] > player.rect.centerx:
            player.speedx = 1
            pygame.draw.circle(screen, pygame.Color('blue'), (destination[0], destination[1]), 10)
        if destination[0] < player.rect.centerx:
            player.speedx = -1
            pygame.draw.circle(screen, pygame.Color('blue'), (destination[0], destination[1]), 10)
        elif destination[0] == player.rect.centerx:
            player.speedx = 0
            stop_x = True
        if destination[1] > player.rect.centery:
            player.speedy = 1
            pygame.draw.circle(screen, pygame.Color('blue'), (destination[0], destination[1]), 10)
        if destination[1] < player.rect.centery:
            player.speedy = -1
            pygame.draw.circle(screen, pygame.Color('blue'), (destination[0], destination[1]), 10)
        elif destination[1] == player.rect.centery:
            player.speedy = 0
            stop_y = True
        return [stop_x, stop_y]

    def destination_ai(self, bases, ai, player, fps):
        # if (sqrt((player.rect.centerx - ai.rect.centerx) ** 2 + (player.rect.centery - ai.rect.centery) ** 2)) \
        #         <= 300:
        #     dest = self.movement_ai([player.rect.centerx, player.rect.centery], ai, fps)
        #     self.battle = True
        # else:
            distance = []
            for i in range(len(bases)):
                ai_pos_x = ai.rect.centerx // self.cell_size
                ai_pos_y = ai.rect.centery // self.cell_size
                dist = [ai_pos_x - bases[i].rect.centerx // self.cell_size, ai_pos_y - bases[i].rect.centery //
                        self.cell_size]
                if [bases[i].rect.centerx // self.cell_size, bases[i].rect.centery // self.cell_size] not in \
                        self.hostile_bases:
                    distance.append(dist)
                    distance.append([bases[i].rect.centerx, bases[i].rect.centery])
            try:
                destination_ai = min(distance)
                a = distance.index(destination_ai)
                dest = self.movement_ai(distance[a + 1], ai, fps)
                self.base_lost(dest, distance[a + 1], bases, player, ai)
            except ValueError:
                self.running = False
                print('Вы проиграли!')

    def movement_ai(self, destination, ai, fps):
        stop_x, stop_y = False, False
        if destination[0] > ai.rect.centerx:
            ai.speedx = 1
        if destination[0] < ai.rect.centerx:
            ai.speedx = -1
        elif destination[0] == ai.rect.centerx:
            ai.speedx = 0
            stop_x = True
        if destination[1] > ai.rect.centery:
            ai.speedy = 1
        if destination[1] < ai.rect.centery:
            ai.speedy = -1
        elif destination[1] == ai.rect.centery:
            ai.speedy = 0
            stop_y = True
        return [stop_x, stop_y]

    def base_taken(self, dest, destination, bases, player, ai):
        if dest[0] and dest[1]:
            player_grid_x = destination[0] // self.cell_size
            player_grid_y = destination[1] // self.cell_size
            for i in range(len(bases)):
                if bases[i].rect.centerx // self.cell_size == player_grid_x and bases[i].rect.centery // \
                        self.cell_size == player_grid_y:
                    bases[i] = Base(bases[i].rect.centerx - self.cell_size // 2, bases[i].rect.centery - self.cell_size
                                    // 2, 'friendly')
                    self.all_sprites = pygame.sprite.Group()
                    self.all_sprites.add(player, ai, bases, self.friendly_missiles)
                    if [bases[i].rect.centerx // self.cell_size, bases[i].rect.centery // self.cell_size] in \
                            self.hostile_bases:
                        self.hostile_bases.remove([bases[i].rect.centerx // self.cell_size, bases[i].rect.centery //
                                                   self.cell_size])

    def base_lost(self, dest, destination, bases, player, ai):
        if dest[0] and dest[1]:
            ai_grid_x = destination[0] // self.cell_size
            ai_grid_y = destination[1] // self.cell_size
            for i in range(len(bases)):
                if bases[i].rect.centerx // self.cell_size == ai_grid_x and bases[i].rect.centery // self.cell_size == \
                        ai_grid_y:
                    bases[i] = Base(bases[i].rect.centerx - self.cell_size // 2, bases[i].rect.centery -
                                    self.cell_size // 2, 'hostile')
                    self.all_sprites = pygame.sprite.Group()
                    self.all_sprites.add(player, ai, bases, self.friendly_missiles)
                    self.hostile_bases.append([bases[i].rect.centerx // self.cell_size, bases[i].rect.centery //
                                               self.cell_size])

    def set_pause(self, screen, pause_screen, board, size, ai):
        if not self.pause:
            self.all_sprites.update()
            if not self.ai_detected:
                ai.update()
            pygame.display.flip()
            screen.fill(pygame.Color('gray5'))
            self.all_sprites.draw(screen)
            board.render(screen)
        else:
            f = pygame.font.Font('font/Teletactile.ttf', 24)
            sc_text = f.render('PAUSE', True, pygame.Color('white'))
            pos = sc_text.get_rect(center=(size[0] // 2, size[1] // 2))
            pause_screen.blit(sc_text, pos)
            pygame.display.flip()

    def fog_of_war(self, ai, player, bases, screen):
        if (sqrt((ai.rect.centerx - player.rect.centerx) ** 2 + (ai.rect.centery - player.rect.centery) ** 2)) \
                <= 300:
            self.all_sprites = pygame.sprite.Group()
            self.all_sprites.add(player, bases, ai, self.friendly_missiles)
            pygame.draw.circle(screen, pygame.Color('red'), (ai.rect.centerx, ai.rect.centery), 300, 1)
            self.ai_detected = True
            self.play_contact_lost = True
            if self.play_new_contact:
                self.sound_new_contact.play()
                self.play_new_contact = False
                self.play_contact_lost = True
                self.pause = True
                self.all_sprites.draw(screen)
        else:
            self.all_sprites = pygame.sprite.Group()
            self.all_sprites.add(player, bases, self.friendly_missiles)
            self.ai_detected = False
            self.play_new_contact = True
            if self.play_contact_lost:
                self.sound_contact_lost.play()
                self.play_contact_lost = False

        pygame.draw.circle(screen, pygame.Color('blue'), (player.rect.centerx, player.rect.centery), 300, 1)
        pygame.draw.circle(screen, pygame.Color('blue'), (player.rect.centerx, player.rect.centery), 1050, 1)

    def main(self):
        pygame.init()
        pygame.mixer.init()
        size = 1400, 800
        screen = pygame.display.set_mode(size)
        pause_screen = pygame.display.set_mode(size)
        pygame.display.set_caption("CW")
        clock = pygame.time.Clock()

        self.cell_size = 75
        self.cells_x = size[0] // self.cell_size
        self.cells_y = size[1] // self.cell_size
        board = Board(self.cells_x, self.cells_y)
        board.set_view(0, 0, self.cell_size)

        fps = 60

        self.all_sprites = pygame.sprite.Group()
        player = Player()
        bases = []
        self.friendly_missiles = []
        self.hostile_missiles = []
        for i in range(10):
            x = random.randint(0, self.cells_x - 1) * self.cell_size
            y = random.randint(0, self.cells_y - 1) * self.cell_size
            bases.append(Base(x, y, 'neutral'))
        ai = AI(board)
        self.all_sprites.add(player, bases)

        self.sound_new_contact = pygame.mixer.Sound('sound/new_radar_contact.wav')
        self.sound_contact_lost = pygame.mixer.Sound('sound/contact_lost.wav')
        self.sound_fire_VLS = pygame.mixer.Sound('sound/FireVLS.wav')

        destination_player = player.rect.center
        self.running = True
        self.pause = False
        start = True
        self.hostile_bases = []
        self.ai_detected = False
        self.play_new_contact, self.play_contact_lost = True, False
        self.battle = False
        self.missile = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        destination_player = event.pos
                    if event.button == 3:
                        destination_missile = event.pos
                        self.missile = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause

            if self.missile:
                self.missile_launch(destination_missile, player, bases)
                self.missile = False

            dest = self.movement_player(destination_player, player, screen)

            self.friendly_missile_movement(screen, MissileFriendly)

            self.base_taken(dest, destination_player, bases, player, ai)

            self.destination_ai(bases, ai, player, fps)

            self.fog_of_war(ai, player, bases, screen)

            clock.tick(fps)

            self.set_pause(screen, pause_screen, board, size, ai)

            if start:
                self.pause = True
                start = False


if __name__ == '__main__':
    Run().main()
