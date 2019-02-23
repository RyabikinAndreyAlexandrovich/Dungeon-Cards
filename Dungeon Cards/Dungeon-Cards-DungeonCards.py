import os
import random
import sys
import pygame


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


class Board:
    # создание поля
    def __init__(self):
        self.width = 3
        self.height = 3
        self.board = [[0] * 3 for _ in range(3)]
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.sprites = pygame.sprite.Group()
        self.counter = 0
        self.hero = None
        self.monster_n_items = None
        self.items = None
        self.lvl = None
        self.case = None

    def new_board_generate(self, hero, monster_n_items, items, lvl, case):
        self.hero = hero
        self.monster_n_items = monster_n_items
        self.items = items
        self.lvl = lvl
        self.case = case
        for j in range(3):
            for i in range(3):
                if i == 1 and j == 1:
                    self.board[j][i] = self.hero
                else:
                    thing = random.choice(self.monster_n_items)  # список монстров и предметов
                    if thing not in items and self.counter < 7:
                        thing = self.monster_generate(thing)
                        self.counter += 1
                    elif thing in case:
                        thing = self.box_generate(thing)
                    else:
                        thing = self.weapon(thing)
                    self.board[i][j] = thing
                try:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = sprites[self.board[i][j]['Name']]
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = 151 + i * 100
                    sprite.rect.y = 151 + j * 100
                    self.sprites.add(sprite)
                except:
                    pass

    def box_generate(self, thing):
        if thing == "money":
            thing = {"Name": "money", "cost": random.randint(1 + self.lvl, (self.lvl + 1) * 2)}
        elif thing == "bad box":
            thing = {"Name": "bad box", "content": random.choice(bad_box)}
        else:
            thing = {"Name": "good box", "content": random.choice(good_box)}
        return thing

    def monster_generate(self, name, spec=False):
        return {"Name": name, "HP": self.lvl + 2, "SPECIAL": spec}

    def weapon(self, thing):
        return {"Name": thing, "Power": random.randint(self.lvl + 2, (self.lvl + 1) * 4)}

    def fight(self, hero_location, location):
        if self.hero['weapon'] is not False:
            damage = self.board[location[0]][location[1]]["HP"] - self.board[hero_location[0]][hero_location[1]]["weapon"]
            if damage >= 0:
                self.board[hero_location[0]][hero_location[1]]['HP'] -= damage
                self.board[hero_location[0]][hero_location[1]]['weapon'] = False
            else:
                self.board[hero_location[0]][hero_location[1]]["weapon"] = -damage
        else:
            self.board[hero_location[0]][hero_location[1]]["HP"] -= self.board[location[0]][location[1]]["HP"]
        if self.board[hero_location[0]][hero_location[1]]["HP"] > 0:
            self.counter -= 1
            self.board[location[0]][location[1]] = None

    def item_gen(self, location):
        thing = random.choice(self.monster_n_items)  # список монстров и предметов
        if thing not in items and self.counter < 7:
            thing = self.monster_generate(thing)
            self.counter += 1
        elif thing in case:
            thing = self.box_generate(thing)
        else:
            thing = self.weapon(thing)
        self.board[location[0]][location[1]] = thing

    def cell_coord_gen(self, location,
                       side):  # проверь пожалуйста эту функцию потому что у меня есть ощущение что я ошибся с индексами
        if side == "down":
            self.board[location[0]][location[1] + 1] = self.board[location[0]][location[1]]
            if location[1] == 1:
                self.board[location[0]][location[1]] = self.board[location[0]][location[1]-1]
            if location[0] == 0:
                self.item_gen([0, 0])
            if location[0] == 2:
                self.item_gen([2, 0])
            if location[0] == 1:
                self.board[location[0]][0] = self.board[0][0]
                self.item_gen([0, 0])
        if side == "up":
            self.board[location[0]][location[1] - 1] = self.board[location[0]][location[1]]
            if location[1] == 1:
                self.board[location[0]][location[1]] = self.board[location[0]][location[1] + 1]
            self.item_gen([location[0], 2])
        if side == "right":
            self.board[location[0] + 1][location[1]] = self.board[location[0]][location[1]]
            if location[0] == 1:
                self.board[location[0]][location[1]] = self.board[location[0] - 1][location[1]]
            self.item_gen([0, location[1]])
        if side == "left":
            self.board[location[0]-1][location[1]] = self.board[location[0]][location[1]]
            if location[0] == 1:
                self.board[location[0]][location[1]] = self.board[location[0] + 1][location[1]]
            self.item_gen([2, location[1]])
    
    def update(self):
        self.sprites = pygame.sprite.Group()
        for j in range(3):
            for i in range(3):
                try:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = sprites[self.board[i][j]['Name']]
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = 151 + i * 100
                    sprite.rect.y = 151 + j * 100
                    self.sprites.add(sprite)
                except Exception as e:
                    pass
                
    def open_box(self, box_location):
        content = self.board[box_location[0]][box_location[1]]['content']
        if content == 'money':
            thing = self.box_generate(content)
        if content in ('sword', 'golden sword'):
            thing = self.weapon(content)
        if content in bad_box:
            thing = self.monster_generate(content)
        self.board[box_location[0]][box_location[1]] = thing
    
    def get_money(self, coin, money_location):
        coin += self.board[money_location[0]][money_location[1]]['cost']
        self.board[money_location[0]][money_location[1]] = None
        return coin
    
    def get_weapon(self, hero_location, item_location):
        self.board[hero_location[0]][hero_location[1]]['weapon'] = \
            self.board[item_location[0]][item_location[1]]['Power']
        self.board[item_location[0]][item_location[1]] = None


def move(side):
    global coin
    location1 = location
    if side == "up" and location[1] > 0:
        new_location = [location[0], location[1]-1]
        if board.board[new_location[0]][new_location[1]]['Name'] in ('good box', 'bad box'):
            board.open_box(new_location)
        elif board.board[new_location[0]][new_location[1]]['Name'] == 'money':
            coin = str(board.get_money(int(coin), new_location))
        elif board.board[new_location[0]][new_location[1]]['Name'] in ('sword', 'golden sword'):
            board.get_weapon(location, new_location)
        else:
            board.fight(location, new_location)
        if board.board[new_location[0]][new_location[1]] is None:
            board.cell_coord_gen(location1, side)
            location[1] -= 1
            
    elif side == "left" and location[0] > 0:
        new_location = [location[0] - 1, location[1]]
        if board.board[new_location[0]][new_location[1]]['Name'] in ('good box', 'bad box'):
            board.open_box(new_location)
        elif board.board[new_location[0]][new_location[1]]['Name'] == 'money':
            coin = str(board.get_money(int(coin), new_location))
        elif board.board[new_location[0]][new_location[1]]['Name'] in ('sword', 'golden sword'):
            board.get_weapon(location, new_location)
        else:
            board.fight(location, new_location)
        if board.board[new_location[0]][new_location[1]] is None:
            board.cell_coord_gen(location1, side)
            location[0] -= 1
        
    elif side == "right" and location[0] < 2:
        new_location = [location[0] + 1, location[1]]
        if board.board[new_location[0]][new_location[1]]['Name'] in ('good box', 'bad box'):
            board.open_box(new_location)
        elif board.board[new_location[0]][new_location[1]]['Name'] == 'money':
            coin = str(board.get_money(int(coin), new_location))
        elif board.board[new_location[0]][new_location[1]]['Name'] in ('sword', 'golden sword'):
            board.get_weapon(location, new_location)
        else:
            board.fight(location, new_location)
        if board.board[new_location[0]][new_location[1]] is None:
            board.cell_coord_gen(location1, side)
            location[0] += 1

    elif side == "down" and location[1] < 2:
        new_location = [location[0], location[1] + 1]
        if board.board[new_location[0]][new_location[1]]['Name'] in ('good box', 'bad box'):
            board.open_box(new_location)
        elif board.board[new_location[0]][new_location[1]]['Name'] == 'money':
            coin = str(board.get_money(int(coin), new_location))
        elif board.board[new_location[0]][new_location[1]]['Name'] in ('sword', 'golden sword'):
            board.get_weapon(location, new_location)
        else:
            board.fight(location, new_location)
        if board.board[new_location[0]][new_location[1]] is None:
            board.cell_coord_gen(location1, side)
            location[1] += 1
    board.board[location[0]][location[1]] = board.board[location1[0]][location1[1]]


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


def update():
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
    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress('w', coin, lvls)
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
                progress('w', coin, lvls)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 99 < event.pos[1] < 560 and (event.pos[1] - 100) // 51 <= len(lvls) - 1:
                    process((event.pos[1] - 100) // 51)
                    break


def process(lvl):
    screen.fill((10, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), ((150, 150), (300, 300)))
    hero = {"Name": "knight", "HP": 10, "weapon": False, "armor": False, "condition": False}
    board.new_board_generate(hero, things, items, lvl, case)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress('w', coin, lvls)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 273:
                    move("up")
                if event.key == 274:
                    move("down")
                if event.key == 275:
                    move("right")
                if event.key == 276:
                    move("left")
        if board.board[location[0]][location[1]]["HP"] <= 0:
            game_over()
            break
        screen.fill((10, 10, 10))
        for y in range(3):
            for x in range(3):
                pygame.draw.rect(screen, (100, 100, 100), ((151 + x * 100, 151 + y * 100), (98, 98)))
        coin, lvls = progress('r')
        update()
        board.update()
        board.sprites.draw(screen)
        other_sprites.draw(screen)
        pygame.display.flip()
        progress('w', coin, lvls)


def game_over():
    global location
    screen.fill((10, 10, 10))
    intro_text = 'GAME OVER'
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 3, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 100
    screen.blit(string_rendered, intro_rect)
    intro_text = "TAP TO RESTART"
    font = pygame.font.Font(None, 20)
    string_rendered = font.render(intro_text, 2, pygame.Color('grey'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 500
    intro_rect.x = 100
    screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    progress('w', coin, lvls)
    print(coin)
    location = [1, 1]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start_screen()


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
good_box = ('money', 'sword', 'golden sword')
bad_box = ('zombie', 'spider', 'skeleton', 'sky', 'khthulhu')
things = ('sword', 'golden sword', 'zombie', 'spider', 'skeleton', 'sky', 'money', 'good box', 'bad box', 'khthulhu')
case = ('money', 'good box', 'bad box')
images = ['money', 'knight', 'start', 'good box', 'bad box', 'sword', 'sky', 'golden sword', 'zombie', 'spider',
          'skeleton', 'khthulhu']
sprites = {}
for i in images:
    try:
        sprites[i] = load_image(i)
    except:
        pass

money = Other('money')
money.rect.x = money.rect.y = 20

coin, lvls = progress('r')
location = [1, 1]
board = Board()
start_screen()