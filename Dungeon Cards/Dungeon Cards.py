import os
import random
import sys
import pygame


def progress(mode, coin=None, lvls=None):
    if mode == 'r':
        with open('data/progress/statistic', 'r') as progress:
            progress = [line.strip() for line in progress]
            coin = progress[0]
            lvls = progress[2:]
            return (coin, lvls)
    if mode == 'w':
        with open('data/progress/statistic', 'w') as progress:
            progress.write('{}\nlvl:\n'.format(coin))
            for lvl in lvls:
                progress.write('{}\n'.format(lvl))


def load_image(name, colorkey=None):
    name += '.png'
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def update(coin):
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(coin, 2, pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 28
    intro_rect.x = 60
    screen.blit(string_rendered, intro_rect)


def start_screen():
    knight = StartSprites('knight')
    knight.rect.x = knight.rect.y = 260
    start = StartSprites('start')
    start.rect.x = 270
    start.rect.y = 350
    intro_text = "Dungeon Cards"
    screen.fill((10, 10, 10))
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 2, pygame.Color('pink'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 168
    screen.blit(string_rendered, intro_rect)
    start_sprites.draw(screen)
    other_sprites.draw(screen)
    update(coin)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 270 <= event.pos[0] <= 318 and\
                        350 <= event.pos[1] <= 398:
                    lvl_menu()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def lvl_menu():
    y_pos = 100
    for i in range(9):
        pygame.draw.rect(screen, (50, 50, 50), ((0, y_pos), (600, y_pos + 50)))
        pygame.draw.rect(screen, (0, 0, 0), ((0, y_pos + 50), (600, y_pos + 50)))
        intro_text = "level {}".format(i + 1)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(intro_text, 2, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y_pos + 10
        intro_rect.x = 100
        screen.blit(string_rendered, intro_rect)
        try:
            intro_text = "best score: {}".format(lvls[i])
            font = pygame.font.Font(None, 20)
            string_rendered = font.render(intro_text, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = y_pos + 20
            intro_rect.x = 400
            screen.blit(string_rendered, intro_rect)
        except:
            intro_text = "LOCKED"
            font = pygame.font.Font(None, 20)
            string_rendered = font.render(intro_text, 2, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = y_pos + 10
            intro_rect.x = 10
            screen.blit(string_rendered, intro_rect)
        y_pos += 51
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 99 < event.pos[1] < 560 and (event.pos[1] - 100) // 51 <= len(lvls) - 1:
                    print((event.pos[1] - 100) // 51)
                    print(lvls)
                    process(lvl((event.pos[1] - 100) // 51))
                    break


def lvl(lvl):
    rules = 0


def process(rules):
    screen.fill((10, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), ((150, 150), (300, 300)))
    for y in range(3):
        for x in range(3):
            pygame.draw.rect(screen, (100, 100, 100), ((151 + x * 100, 151 + y * 100), (98, 98)))
    other_sprites.draw(screen)
    update(coin)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class StartSprites(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(start_sprites)
        self.image = sprites[type]
        self.rect = self.image.get_rect()


class Other(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(other_sprites)
        self.image = sprites[type]
        self.rect = self.image.get_rect()


class Character(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(all_sprites)
        self.image = sprites[type]
        self.rect = self.image.get_rect().move(260, 260)


pygame.init()
size = WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50

all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
other_sprites = pygame.sprite.Group()

things = ('sword', 'golden sword', 'zombie', 'spider', 'skeleton', 'sky', 'money', 'good box', 'bad box')

images = ['money', 'knight', 'start', 'good box', 'bad box']
sprites = {}
for i in images:
    sprites[i] = load_image(i)

money = Other('money')
money.rect.x = money.rect.y = 20

coin, lvls = progress('r')

start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 273:
                pass
            if event.key == 274:
                pass
            if event.key == 275:
                pass
            if event.key == 276:
                pass
    screen.fill((10, 10, 10))
    coin, lvls = progress('r')
    update(coin)
    pygame.display.flip()
    progress('w', coin, lvls)
pygame.quit()
