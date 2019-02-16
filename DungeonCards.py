import os
import random
import sys
import pygame


class Board:
    # создание поля
    def __init__(self):
        self.width = 3
        self.height = 3
        self.board = [[0] * 3 for _ in range(3)]
        self.left = 0
        self.top = 0
        self.cell_size = 0

    def new_board_generate(self, hero, monster_n_items, items, lvl, case):
        counter = 0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    self.board[i][j] = hero
                else:
                    thing = random.choice(monster_n_items)  # список монстров и предметов
                    if thing not in items and counter < 7:
                        thing = self.monster_generate(thing, lvl)
                        counter += 1
                    elif thing in case:  # короче он почему то когда j = 1 сюда не заходит. почему я хз
                        thing = self.box_generate(thing, lvl)
                    else:
                        thing = random.choice(items)
                    self.board[i][j] = thing
        print(self.board)

    def box_generate(self, thing, lvl):
        if thing == "money":
            thing = {"Name": "money", "cost": random.randint(1 + lvl, (lvl + 1) * 2)}
        elif thing == "bad box":
            thing = {"Name": "bad box", "content": random.choice(things)}
        else:
            thing = {"Name": "Good box", "content": random.choice(items)}
        return thing

    def monster_generate(self, name, lvl, spec=False):
        thing = {"Name": name, "HP": lvl + 2, "SPECIAL": spec}
        return thing

    def new_cell_generate(self, cell_coord):
        self.board[cell_coord[0]][cell_coord[1]]

    def fight(self, hero):
        if hero['weapon'] != False:
            damage = self.board[location[0]][location[1]]["HP"] - hero["weapon"]
            if damage >= 0:
                hero['hp'] -= damage
                hero['weapon'] = False
            else:
                hero["weapon"] = damage
        else:
            hero['hp'] -= self.board[location[0]][location[1]]["HP"]
    # def item_gen(self):
    #     return random.choice(items)

    def cell_coord_gen(self, location,
                       side):  # проверь пожалуйста эту функцию потому что у меня есть ощущение что я ошибся с индексами
        if side == "down":
            self.board[location[0]][location[1]] = self.board[location[0]][location[1] - 1]
            if location[1] == 1:
                self.board[location[0]][location[1] - 1] = self.board[location[0]][location[1] - 2]
            return [location[0], 0]
        if side == "up":
            self.board[location[0]][location[1]] = self.board[location[0]][location[1] + 1]
            if location[1] == 1:
                self.board[location[0]][location[1] + 1] = self.board[location[0]][location[1] + 2]
            return [location[0], 0]
        if side == "right":
            if location[1] == 2:
                self.board[location[0]][location[1]] = self.board[location[0] - 1][location[1]]
                return [location[0], location[1]]
            if location[1] == 1:
                self.board[location[0], location[1]] = self.board[location[0] - 2, location[1]]
                if location[0] == 1:
                    self.board[location[0] - 1, location[1]] = self.board[location[0] - 1, location[1]]

                self.board[location[0], location[1]] = self.board[location[0] - 1, location[1]]


def move(side):
    if side == "up" and location[1] < 0:
        location[1] -= 1
        if Board.board[location[0]][location[1]] in items:
            Board.item_gen()
        else:
            Board.fight()
        Board.cell_coord_gen(location)
    elif side == "left" and location[0] < 0:
        location[0] -= 1

        Board.cell_coord_gen(location)
    elif side == "right" and location[0] > 2:
        location[0] += 1
        Board.cell_coord_gen(location)
    elif side == "down" and location[1] > 2:
        location[1] += 1
        Board.cell_coord_gen(location, side)


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
                if 270 <= event.pos[0] <= 318 and \
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
                    process((event.pos[1] - 100) // 51)
                    break


def lvl1():
    pass


def process(lvl):
    board = Board()
    screen.fill((10, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), ((150, 150), (300, 300)))
    hero = {"hp": 10, "weapon": False, "armor": False, "condition": False}
    board.new_board_generate(hero, things, items, lvl, case)
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
items = ['money', 'good box', 'bad box', 'sword', 'golden sword']
all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
other_sprites = pygame.sprite.Group()
good_box = ['money', 'sword', 'golden sword']
things = ('sword', 'golden sword', 'zombie', 'spider', 'skeleton', 'sky', 'money', 'good box', 'bad box')
case = ('money', 'good box', 'bad box')
images = ['money', 'knight', 'start', 'good box', 'bad box']
sprites = {}
for i in images:
    sprites[i] = load_image(i)

money = Other('money')
money.rect.x = money.rect.y = 20

coin, lvls = progress('r')
location = [1, 1]
start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 273:
                move("up")
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
