import pygame, sys, random, os
mode2index = {"Run":0, "Attack":1, "Hit":2, "Dead":3}
coordinate = [[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

def pos2coord(pos):
    x = int((pos[1] - 97.6584) / 124.7363)
    y = int((pos[0] - 136.9868) / 148.5726)
    return x, y

class Character:
    def __init__(self, hp, pos, damage, fps):
        self.hp = hp
        self.pos = pos
        self.damage = damage
        self.index = 0
        self.fps = fps

class Hero(Character):
    def __init__(self, hp, pos, damage, surface, fps):
        self.characterSide = "hero"
        super().__init__(hp, pos, damage, fps)
        self.surface = [pygame.image.load(f"image/{self.characterSide}/{surface[0]}/{surface[0]}{i}.png").convert_alpha() for i in range(surface[1] + 1)]
        self.rect = self.surface[0].get_rect(midbottom=self.pos)
        self.show = self.surface[0]
        x, y = pos2coord(self.pos)
        self.coord = (x, y)
        self.round = 0


class Bullet:
    def __init__(self, rect, surface, side, damage, speed_x, speed_y=0):
        self.index = 0
        self.name = "bullet"
        self.animal = surface[0]
        self.surface = [pygame.image.load(f"image/{side}/{self.name}/{surface[0]}_{self.name}.png").convert_alpha()]
        self.show = self.surface[0]
        self.rect = self.show.get_rect(center=rect.center)
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
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1])]
                self.load_dead = True
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0] - 1):
                pass
            else:
                self.index += 1
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)

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
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)

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
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)

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
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1])]
                self.load_dead = True
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0] - 1):
                pass
            else:
                self.index += 1
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)

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
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.rect.midbottom)
        self.rect.centerx += self.speed

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
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1])]
                self.load_dead = True
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0] - 1):
                pass
            else:
                self.index += 1
        self.show = self.surface[self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)

    def skill(self):
        for rule in heroes:
            rule.hp = rule.hp+0.05 if rule.hp <= 100 else rule.hp


class Enemy(Character):
    def __init__(self, name, hp, pos, damage, speed, fps):
        super().__init__(hp, pos, damage, fps)
        self.name = name
        self.characterSide = "enemy"
        self.show_mode = "Run"
        self.speed = speed;
        self.is_dead = False
        self.is_dead_load = False
        self.surfaces = {}
        all_mode = ["Run", "Attack", "Hit", "Dead"]
        for i, mode in enumerate(all_mode):
            project_dir = f"image/{self.characterSide}/{self.name}/{mode}"
            file_count = 0
            for folder, _, filenames in os.walk(project_dir):
                for filename in filenames:
                    if filename.endswith(".png"):
                        file_count += 1
            self.surfaces[mode] = [pygame.image.load(f'{project_dir}/{j + 1}.png').convert_alpha() for j in range(file_count)]
        self.show = self.surfaces[self.show_mode][self.index]
        self.rect = self.show.get_rect(midbottom=self.pos)


class Crabby(Enemy):
    def __init__(self, pos):
        name = "Crabby"
        hp = 300
        damage = 30
        fps = 90
        speed = -5

        super().__init__(name, hp, pos, damage, speed, fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (len(self.surfaces[self.show_mode])-1):
                self.index = 0
            else:
                self.index += 1
        # else:
        #     if not self.load_dead:
        #         # print("load")
        #         self.surface = [
        #             pygame.image.load(f"image/{self.characterSide}/{self.name}/{self.show_mode}/{i}.png").convert_alpha()
        #             for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1])]
        #         self.load_dead = True
        #     if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0] - 1):
        #         pass
        #     else:
        #         self.index += 1

        self.show = self.surfaces[self.show_mode][self.index]
        # self.rect = self.show.get_rect(midbottom=self.pos)
        self.rect.x += self.speed

class Fierce_Tooth(Enemy):
    def __init__(self, pos):
        name = "Fierce Tooth"
        hp = 300
        damage = 30
        fps = 90
        speed = -5

        super().__init__(name, hp, pos, damage, speed, fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (len(self.surfaces[self.show_mode])-1):
                self.index = 0
            else:
                self.index += 1
        # else:
        #     if not self.load_dead:
        #         # print("load")
        #         self.surface = [
        #             pygame.image.load(f"image/{self.characterSide}/{self.name}/{self.show_mode}/{i}.png").convert_alpha()
        #             for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1])]
        #         self.load_dead = True
        #     if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0] - 1):
        #         pass
        #     else:
        #         self.index += 1

        self.show = self.surfaces[self.show_mode][self.index]
        # self.rect = self.show.get_rect(midbottom=self.pos)
        self.rect.x += self.speed


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("EGG DEFENSE")
clock = pygame.time.Clock()
bg_surface = pygame.image.load('image/backgroud.png').convert()

heroes = []
heroesFPS = []
heroesBullet = []
heroesBulletFPS = []
enemies = []
enemiesFPS = []
FPSCounter = 0
all_enemies = ["Crabby", "Fierce Tooth", "Pink Star", "Seashell", "Whale"]
all_heroes = ["dog", "frog", "bird", "mushroom", "rino", "cat"]

def create_hero(animal, x, y):
    if animal == 'dog':
        heroes.append(Dog(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'frog':
        heroes.append(Frog(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'bird':
        heroes.append(Bird(80, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'mushroom':
        heroes.append(Mushroom(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1
    elif animal == 'rino':
        heroes.append(Rino(50, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
    elif animal == 'cat':
        heroes.append(Cat(10, (211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3), 12))
        coordinate[x][y] = 1

    global FPSCounter
    heroesFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, heroes[-1].fps)
    FPSCounter += 1

def create_enemy(name, row):
    default_x = 1350
    match(name):
        case "Crabby":
            enemies.append(Crabby((default_x, 222.3947 + 124.7363 * row - 3)))
        case "Fierce Tooth":
            enemies.append(Fierce_Tooth((default_x, 222.3947 + 124.7363 * row - 3)))

    global FPSCounter
    enemiesFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, enemies[-1].fps)
    FPSCounter += 1

create_enemy("Crabby", 3)
create_enemy("Fierce Tooth", 2)
def bullet_update():
    global FPSCounter
    for rule in heroes:
        if rule.animal in ("dog", "bird", "frog") and (rule.round != rule.index):
            rule.round = rule.index
            if rule.index == (len(rule.surface)//2):
                heroesBullet.append(
                Bullet(rule.rect, (rule.animal, 3), rule.characterSide, rule.damage, rule.speed_x, rule.speed_y))

    if heroesBullet:
        for bullet in heroesBullet:
            bullet.rect.centerx += bullet.speed_x
            if bullet.rect.left >= 1280:
                heroesBullet.remove(bullet)

def main():
    while True:
        screen.blit(bg_surface, (0, 0))
        for rule in heroes:
            if rule.hp <= 0 and (not rule.isDead):
                rule.index = 0
                rule.isDead = True
            if rule.animal == "cat":
                rule.skill()
            else:
                print(rule.hp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for index, ruleFPS in enumerate(heroesFPS):
                if event.type == ruleFPS:
                    heroes[index].animation()

            for index, ruleFPS in enumerate(enemiesFPS):
                if event.type == ruleFPS:
                    enemies[index].animation()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # print(x, y)
                if (x >= 136.9868) and (x <= 136.9868+892.2375) and (y >= 97.6584) and (y <= 97.6584+623.6815):
                    x, y = pos2coord(event.pos)
                    if not coordinate[x][y]:
                        animal = random.choice(all_heroes)
                        create_hero(animal, x, y)

        bullet_update()
        for bullet in heroesBullet:
            screen.blit(bullet.show, bullet.rect)

        for rule in heroes:
            screen.blit(rule.show, rule.rect)
        for rule in enemies:
            screen.blit(rule.show, rule.rect)


        for index, rule in enumerate(heroes):
            if rule.isDead and (len(rule.characterAnimation) == 1 or rule.index == (rule.characterAnimation[1][1]-rule.characterAnimation[1][0]-1)):
                heroes.remove(rule)
                coordinate[rule.coord[0]][rule.coord[1]] = 0
                heroesFPS.remove(heroesFPS[index])

        pygame.display.update()
        clock.tick(90)

if __name__ == "__main__":
    main()