import pygame, sys, random

coordinate = [[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

def pos2coord(pos):
    x = int((pos[1] - 97.6584) / 124.7363)
    y = int((pos[0] - 136.9868) / 148.5726)
    return x, y

class Character(pygame.sprite.Sprite):
    def __init__(self, hp, pos, damage, fps):
        super().__init__()
        self.hp = hp
        self.pos = pos
        self.damage = damage
        self.index = 0
        self.fps = fps

class Hero(Character):
    def __init__(self, hp, pos, damage, surface, fps):
        self.characterSide = "hero"
        super().__init__(hp, pos, damage, fps)
        self.surface = [pygame.image.load(f"image/{self.characterSide}/{surface[0]}/{surface[0]}{i}.png").convert_alpha()
                        for i in range(surface[1] + 1)]
        self.rect = self.surface[0].get_rect(midbottom=self.pos)
        self.image = self.surface[0]
        x, y = pos2coord(self.pos)
        self.coord = (x, y)
        self.round = 0

class Enemy(Character):
    def __init__(self, hp, pos, damage, file, speed):
        super().__init__(hp, pos, damage, file)
        self.speed = speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, surface, side, damage, speed_x, speed_y=0, index=0):
        super().__init__()
        self.index = 0
        self.name = "bullet"
        self.animal = surface[0]
        if surface[0] != "bee":
            self.surface = [pygame.image.load(f"image/{side}/{self.name}/{surface[0]}_{self.name}.png").convert_alpha()]
        else:
            self.surface = [pygame.image.load(f"image/{side}/{self.name}/{surface[0]}_{self.name}{index}.png").convert_alpha()]
        self.image = self.surface[0]
        self.rect = self.image.get_rect(center=rect.center)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.side = side
        self.damage = damage

class Dog(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 11), (12, 18)]
        self.animal = "dog"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 7
        self.speed_y = 0
        fps = 100
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Frog(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 11)]
        self.animal = "frog"
        self.isDead = False
        self.speed_x = 5
        self.speed_y = 0
        fps = 100
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Bird(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 7)]
        self.animal = "bird"
        self.isDead = False
        self.speed_x = 8
        self.speed_y = 0
        fps = 100
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Mushroom(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 7), (8, 16)]
        self.animal = "mushroom"
        self.isDead = False
        self.load_dead = False
        fps = 200
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 3
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Rino(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 5)]
        self.animal = "rino"
        self.isDead = False
        self.speed = 8
        fps = 10
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.rect.midleft[0] <= 1280:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            self.isDead = True
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self.rect.centerx += self.speed

    def skill(self):
        pass

class Cat(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 7), (8, 14)]
        self.animal = "cat"
        self.isDead = False
        self.load_dead = False
        fps = 200
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    def skill(self):
        for rule in heroes:
            rule.hp = rule.hp+0.03 if rule.hp <= 100 else rule.hp

class Fox(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 10), (11, 17)]
        self.animal = "fox"
        self.isDead = False
        self.load_dead = False
        fps = 100
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    def skill(self):
        pass

class Turtle(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 15), (16, 19)]
        self.animal = "turtle"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 7
        self.speed_y = 0
        fps = 100
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] +1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    def skill(self):
        pass

class Bee(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 7), (8, 12)]
        self.animal = "bee"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 5
        self.speed_y = (-5, 0, 5)
        fps = 200
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.hp -= 2
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    def skill(self, rule, direction):
        rule.round = rule.index
        if rule.index == (len(self.surface) // 2):
            heroesBullet.add(
                Bullet(rule.rect, (self.animal, 3), self.characterSide, rule.damage, self.speed_x, self.speed_y[direction], direction))

class Turkey(Hero):
    def __init__(self, hp, pos, damage):
        self.characterAnimation = [(0, 13), (14, 19)]
        self.animal = "turkey"
        self.isDead = False
        self.load_dead = False
        self.speed = 10
        fps = 10
        super().__init__(hp, pos, damage, (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.rect.midbottom[1] <= 720:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.rect.centery += self.speed
        else:

            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1]+1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1]-self.characterAnimation[1][0]):
                self.isDead = True
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def skill(self):
        pass

class Guidance_block:
    def __init__(self):
        self.image = pygame.Surface((148.5726, 124.7363), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 128))
        self.rect = self.image.get_rect()
    def update(self):
        x, y = pygame.mouse.get_pos()
        if (x >= 136.9868) and (x <= 136.9868 + 892.2375) and (y >= 97.6584) and (y <= 97.6584 + 623.6815):
            x, y = pos2coord((x, y))
            if not coordinate[x][y]:
                self.image.fill((255, 255, 255, 40))
                self.rect.x = y * 148.5726 + 139
                self.rect.y = x * 124.7363 + 100
                screen.blit(self.image, self.rect)

def create_hero(animal, x, y):
    if animal == 'dog':
        heroes.add(Dog(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'frog':
        heroes.add(Frog(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'bird':
        heroes.add(Bird(80, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'mushroom':
        heroes.add(Mushroom(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'rino':
        heroes.add(Rino(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 0
    elif animal == 'turkey':
        heroes.add(Turkey(50, (211.2731 + 148.5726 * y, 0), 12))
        coordinate[x][y] = 0
    elif animal == 'cat':
        heroes.add(Cat(10, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'fox':
        heroes.add(Fox(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'turtle':
        heroes.add(Turtle(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'bee':
        heroes.add(Bee(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1

    global FPSCounter
    heroesFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, heroes.sprites()[-1].fps)
    FPSCounter += 1

def bullet_update():
    global FPSCounter
    for rule in heroes.sprites():
        if rule.animal in ("dog", "bird", "frog") and (rule.round != rule.index):
            rule.round = rule.index
            if rule.index == (len(rule.surface)//2):
                heroesBullet.add(Bullet(rule.rect, (rule.animal, 3), rule.characterSide, rule.damage, rule.speed_x, rule.speed_y))

        elif rule.animal == "bee" and (rule.round != rule.index) and True:   # True: some enemy near the bee
            rule.skill(rule, 0)

    if heroesBullet.sprites():
        for bullet in heroesBullet:
            bullet.rect.centerx += bullet.speed_x
            bullet.rect.centery += bullet.speed_y
            if bullet.rect.left >= 1280:
                bullet.kill()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
bg_surface = pygame.image.load('image/backgroud.png').convert()

heroes = pygame.sprite.Group()
heroesFPS = []
heroesBullet = pygame.sprite.Group()
FPSCounter = 0

all_heroes = ["dog", "frog", "bird", "mushroom", "cat", "bee", "rino", "fox", "turtle", "turkey"]
guidance_block = Guidance_block()

while True:
    screen.blit(bg_surface, (0, 0))
    for rule in heroes.sprites():
        if rule.hp <= 0 and (not rule.isDead):
            rule.index = 0
            rule.isDead = True
        if rule.animal not in ("bird", "frog", "dog", "mushroom", "bee"):
            rule.skill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for index, ruleFPS in enumerate(heroesFPS):
            if event.type == ruleFPS:
                heroes.sprites()[index].animation()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (x >= 139) and (x <= 139+892.2375) and (y >= 100) and (y <= 100+623.6815):
                x, y = pos2coord(event.pos)
                if not coordinate[x][y]:
                    animal = random.choice(all_heroes)
                    create_hero(animal, x, y)

    guidance_block.update()
    bullet_update()
    heroes.draw(screen)
    heroesBullet.draw(screen)

    for index, rule in enumerate(heroes.sprites()):
        if rule.isDead and (len(rule.characterAnimation) == 1 or rule.index == (rule.characterAnimation[1][1]-rule.characterAnimation[1][0])):
            rule.kill()
            coordinate[rule.coord[0]][rule.coord[1]] = 0
            heroesFPS.remove(heroesFPS[index])

    pygame.display.update()
    clock.tick(90)