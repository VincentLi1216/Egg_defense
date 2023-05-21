import pygame, sys, random, os, copy
coordinate = [[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

heroesHP = {"dog": 100, "cat": 50, "mushroom": 100, "bee": 100, "rino": 100,
            "bird": 100, "frog": 100, "fox": 100, "turtle": 100, "turkey": 100}

heroesDamage = {"dog": 100, "cat": 100, "mushroom": 100, "bee": 100, "rino": 100,
            "bird": 100, "frog": 100, "fox": 100, "turtle": 100, "turkey": 100}

cardCD = {"dog": 500, "cat": 100, "mushroom": 1000, "bee": 1000, "rino": 1000,
            "bird": 500, "frog": 500, "fox": 1000, "turtle": 1000, "turkey": 500}

cardCost = {"dog": 500, "cat": 100, "mushroom": 1000, "bee": 1000, "rino": 3000,
            "bird": 500, "frog": 500, "fox": 700, "turtle": 1000, "turkey": 900}

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, surface, side, damage, speed_x, speed_y=0, index=0):
        super().__init__()
        self.index = index
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

class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, rect, path, damage, bullet_speed):
        super().__init__()
        self.rect = copy.deepcopy(rect)
        self.rect.y += 30
        self.image = pygame.image.load(path).convert_alpha()
        self.damage = damage
        self.bullet_speed = bullet_speed

class Dog(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 11), (12, 18)]
        self.animal = "dog"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 7
        self.speed_y = 0
        fps = 100
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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
    def __init__(self, pos):
        self.characterAnimation = [(0, 11)]
        self.animal = "frog"
        self.isDead = False
        self.speed_x = 5
        self.speed_y = 0
        fps = 100
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Bird(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 7)]
        self.animal = "bird"
        self.isDead = False
        self.speed_x = 8
        self.speed_y = 0
        fps = 100
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

class Mushroom(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 7), (8, 16)]
        self.animal = "mushroom"
        self.isDead = False
        self.load_dead = False
        fps = 200
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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
    def __init__(self, pos):
        self.characterAnimation = [(0, 5)]
        self.animal = "rino"
        self.isDead = False
        self.speed = 8
        fps = 10
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

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
    def __init__(self, pos):
        self.characterAnimation = [(0, 7), (8, 14)]
        self.animal = "cat"
        self.isDead = False
        self.load_dead = False
        fps = 200
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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
        target = 0
        while True:
            try:
                if heroes.sprites()[target].animal == "cat":
                    target += 1
                else:
                    break
            except:
                target -= 1
                break
        for index in range(len(heroes.sprites())):
            if heroes.sprites()[index].hp < heroes.sprites()[target].hp and heroes.sprites()[index].animal != "cat":
                target = index
        heroes.sprites()[target].hp = heroes.sprites()[target].hp+10 if heroes.sprites()[target].hp <= heroesHP[heroes.sprites()[target].animal] else heroes.sprites()[target].hp

class Fox(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 10), (11, 17)]
        self.animal = "fox"
        self.isDead = False
        self.load_dead = False
        fps = 100
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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
    def __init__(self, pos):
        self.characterAnimation = [(0, 15), (16, 19)]
        self.animal = "turtle"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 7
        self.speed_y = 0
        fps = 100
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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

class Bee(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 7), (8, 12)]
        self.animal = "bee"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 5
        self.speed_y = (-5, 0, 5)
        fps = 200
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
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
    def __init__(self, pos):
        self.characterAnimation = [(0, 13), (14, 19)]
        self.animal = "turkey"
        self.isDead = False
        self.load_dead = False
        self.speed = 10
        fps = 10
        super().__init__(heroesHP[self.animal], pos, heroesDamage[self.animal], (self.animal, self.characterAnimation[0][1]), fps)

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

class Enemy(Character):
    def __init__(self, name, hp, pos, damage, speed, fps, attack_fps):
        super().__init__(hp, pos, damage, fps)
        self.name = name
        self.characterSide = "enemy"
        self.show_mode = "Run"
        self.speed = speed;
        self.attack_fps = attack_fps
        self.is_dead = False
        self.is_dead_load = False
        self.mode_change_enable = True
        self.indexes_show_after_dead = 10
        self.has_attacked = False
        self.isDead = False #just for testing
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
        self.image = self.surfaces[self.show_mode][self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    # for the animation of the character
    def animation(self, mode, attack_moving_speed = -5, has_bullet = False):
            # if the mode change (different from the last time)
            if mode != self.show_mode:
                # if the character is dead then it's always sticks on the mode "Dead"
                if self.hp > 0:
                    # if the mode_change_enable is True which means that the other mode was loop over
                    if self.mode_change_enable:
                        self.index = 0
                        self.show_mode = mode
                else:
                    self.show_mode = "Dead"

            if self.hp <= 0:
                # load for the first time
                if not self.is_dead_load:
                    self.index = 0
                    self.show_mode = "Dead"
                    self.is_dead_load = True
                # if the dead animation is over
                if self.index >= len(self.surfaces["Dead"]) - 1:
                    self.index += 1
                    # wait for indexes_show_after_dead amount of time
                    if self.index >= (len(self.surfaces["Dead"]) - 1 + self.indexes_show_after_dead):
                        self.is_dead = True
                        # print(f"{self.characterSide} {self.name} is dead")
                else:
                    self.index += 1
            else:
                # image different animation depends on the self.show_mode
                if self.show_mode == "Run":
                    self.rect.x += self.speed
                    if self.index == (len(self.surfaces[self.show_mode]) - 1):
                        self.index = 0
                    else:
                        self.index += 1
                elif self.show_mode == "Attack":
                    self.rect.x += attack_moving_speed
                    # if the attack animation is over then enable self.mode_change_enable = True
                    if self.index == (len(self.surfaces[self.show_mode]) - 1):
                        self.index = 0
                        self.mode_change_enable = True
                        if has_bullet:
                            self.has_attacked = False
                    else:
                        self.mode_change_enable = False
                        self.index += 1
            self.image = self.surfaces[self.show_mode][
                self.index if self.index < len(self.surfaces["Dead"]) else len(self.surfaces["Dead"]) - 1]

class Crabby(Enemy):
    def __init__(self, pos):
        name = "Crabby"
        hp = 200
        damage = 50
        fps = 90
        speed = -5
        attack_fps = 1000
        super().__init__(name, hp, pos, damage, speed, fps, attack_fps)

    def animation(self, mode):
        super().animation(mode)
        # brighten = 128
        # self.surfaces["Run"][0].fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)

class Fierce_Tooth(Enemy):
    def __init__(self, pos):
        name = "Fierce Tooth"
        hp = 200
        damage = 30
        fps = 90
        speed = -7
        attack_fps = 1000

        super().__init__(name, hp, pos, damage, speed, fps, attack_fps)

    def animation(self, mode):
        super().animation(mode)

class Pink_Star(Enemy):
    def __init__(self, pos):
        name = "Pink Star"
        hp = 30
        damage = 30
        fps = 90
        speed = -5
        attack_fps = 1000
        super().__init__(name, hp, pos, damage, speed, fps, attack_fps)

    def animation(self, mode):
        attack_moving_speed = -30
        super().animation(mode,attack_moving_speed)

class Seashell(Enemy):
    def __init__(self, pos):
        name = "Seashell"
        hp = 200
        damage = 30
        fps = 90
        speed = -1
        attack_fps = 1000
        self.bullet_speed = -8
        super().__init__(name, hp, pos, damage, speed, fps, attack_fps)

    def animation(self, mode):
        super().animation(mode, has_bullet=True)

class Whale(Enemy):
    def __init__(self, pos):
        name = "Whale"
        hp = 200
        damage = 30
        fps = 90
        speed = -2
        attack_fps = 2000
        super().__init__(name, hp, pos, damage, speed, fps, attack_fps)

    def animation(self, mode):
        attack_moving_speed = -7
        super().animation(mode, attack_moving_speed)

class Card:
    def __init__(self, animal):
        # super().__init__()
        self.animal = animal
        self.surface = [pygame.image.load(f"image/card/card_{self.animal}{i}.png").convert_alpha() for i in range(10)]
        self.rect = self.surface[0].get_rect(topleft=(0, 12.4222))
        self.image = self.surface[0]
        self.index = 0
        self.fps = cardCD[self.animal]
        self.cost = cardCost[self.animal]

    def cdTime(self):
        if self.index < 9:
            self.index += 1
        else:
            self.index = 9
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

class TmpCard:
    def __init__(self, animal, pos):
        self.animal = animal
        self.image = pygame.image.load(f"image/hero/{self.animal}/{self.animal}0.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

# class Guidance_block:
#     def __init__(self):
#         self.image = pygame.Surface((148.5726, 124.7363), pygame.SRCALPHA)
#         self.image.fill((255, 255, 255, 128))
#         self.rect = self.image.get_rect()
#     def update(self):
#         x, y = pygame.mouse.get_pos()
#         print(x, y)
#         if (x >= 136.9868) and (x <= 136.9868 + 892.2375) and (y >= 97.6584) and (y <= 97.6584 + 623.6815):
#             x, y = pos2coord((x, y))
#             if not coordinate[x][y]:
#                 self.image.fill((255, 255, 255, 40))
#                 self.rect.x = y * 148.5726 + 139
#                 self.rect.y = x * 124.7363 + 100
#                 screen.blit(self.image, self.rect)

def create_hero(animal, x, y):
    if animal == 'dog':
        heroes.add(Dog((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'frog':
        heroes.add(Frog((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'bird':
        heroes.add(Bird((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'mushroom':
        heroes.add(Mushroom((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'rino':
        heroes.add(Rino((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 0
    elif animal == 'turkey':
        heroes.add(Turkey((211.2731 + 148.5726 * y, 0)))
        coordinate[x][y] = 0
    elif animal == 'cat':
        heroes.add(Cat((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'fox':
        heroes.add(Fox((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'turtle':
        heroes.add(Turtle((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'bee':
        heroes.add(Bee((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
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
                heroesBullet.add(
                    Bullet(rule.rect, (rule.animal, 3), rule.characterSide, rule.damage, rule.speed_x, rule.speed_y))

        elif rule.animal == "bee" and (rule.round != rule.index) and True:   # True: some enemy near the bee
            rule.skill(rule, 0)

    if heroesBullet.sprites():
        for bullet in heroesBullet:
            bullet.rect.centerx += bullet.speed_x
            bullet.rect.centery += bullet.speed_y
            if bullet.rect.left >= 1280:
                bullet.kill()

def enemy_bullet_update():
    global FPSCounter
    for rule in enemies.sprites():
        if rule.name in ("Seashell") and rule.show_mode == "Attack" and not rule.has_attacked:
            enemies_bullet.add(Enemy_bullet(rule.rect, "image/enemy/Pearl/Idle/1.png", rule.damage, rule.bullet_speed))
            rule.has_attacked = True

    if enemies_bullet.sprites():
        for bullet in enemies_bullet:
            bullet.rect.x += bullet.bullet_speed
            if bullet.rect.right <= 0:
                enemies_bullet.remove(bullet)
                bullet.kill()

def create_enemy(name, row):
    default_x = 1370
    if name == "Crabby":
        enemies.add(Crabby((default_x, 222.3947 + 124.7363 * row - 3)))
    elif name == "Fierce Tooth":
        enemies.add(Fierce_Tooth((default_x, 222.3947 + 124.7363 * row - 3)))
    elif name == "Pink Star":
        enemies.add(Pink_Star((default_x, 222.3947 + 124.7363 * row - 3)))
    elif name == "Seashell":
        enemies.add(Seashell((default_x, 222.3947 + 124.7363 * row - 3)))
    elif name == "Whale":
        enemies.add(Whale((default_x, 222.3947 + 124.7363 * row - 3)))

    # match(name):
    #     case "Crabby":
    #         enemies.append(Crabby((default_x, 222.3947 + 124.7363 * row - 3)))
    #     case "Fierce Tooth":
    #         enemies.append(Fierce_Tooth((default_x, 222.3947 + 124.7363 * row - 3)))
    #     case "Pink Star":
    #         enemies.append(Pink_Star((default_x, 222.3947 + 124.7363 * row - 3)))
    #     case "Seashell":
    #         enemies.append(Seashell((default_x, 222.3947 + 124.7363 * row - 3)))
    #     case "Whale":
    #         enemies.append(Whale((default_x, 222.3947 + 124.7363 * row - 3)))


    global FPSCounter
    enemiesFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, enemies.sprites()[-1].fps)
    FPSCounter += 1
    enemies_attackFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, enemies.sprites()[-1].attack_fps)
    FPSCounter += 1

def create_card():
    for animal in playerCard:
        cardSet.append(Card(animal))

def card_update():
    global cardSet, disp_card, FPSCounter

    if len(playerCard) <= 5:
        while (len(disp_card) < len(playerCard)):
            b = [card.animal for card in cardSet]
            a = [card.animal for card in disp_card]
            lst = list(set(b).difference(set(a)))
            if lst:
                for animal in lst:
                    disp_card.append(Card(animal))

                    cardsFPS.append(pygame.USEREVENT + FPSCounter)
                    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
                    FPSCounter += 1
                    break

    else:
        while (len(disp_card) < 5):
            if disp_card:
                animal = random.choice(playerCard)
                isSame = False
                for obj in disp_card:
                    if animal == obj.animal:
                        isSame = True
                        break

                if not isSame:
                    disp_card.append(Card(animal))

                    cardsFPS.append(pygame.USEREVENT + FPSCounter)
                    pygame.time.set_timer(pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
                    FPSCounter += 1
                    break
            else:
                animal = random.choice(playerCard)
                disp_card.append(Card(animal))

                cardsFPS.append(pygame.USEREVENT + FPSCounter)
                pygame.time.set_timer(pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
                FPSCounter += 1
                break

    for i in range(len(disp_card)):
        disp_card[i].rect.x = 134.1848 + 86.7772 * i
        screen.blit(disp_card[i].image, disp_card[i].rect)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("EGG DEFENSE")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
bg_surface = pygame.image.load('image/backgroud.png').convert()
cursor_surface = pygame.image.load("image/cursor/cursor2.png").convert_alpha()
cursor_surface = pygame.transform.scale(cursor_surface, (70, 70))
cursor_rect = cursor_surface.get_rect()

heroes = pygame.sprite.Group()
heroesFPS = []
heroesBullet = pygame.sprite.Group()

enemies = pygame.sprite.Group()
enemiesFPS = []
enemies_attackFPS = []
enemies_bullet = pygame.sprite.Group()
enemies_bulletFPS = []
FPSCounter = 0

all_enemies = ["Crabby", "Fierce Tooth", "Pink Star", "Seashell", "Whale"]
# guidance_block = Guidance_block()

create_enemy("Pink Star", 0)
create_enemy("Fierce Tooth", 1)
create_enemy("Crabby", 2)
create_enemy("Whale", 3)
create_enemy("Seashell", 4)

from dataDB import get_data

playerCard = get_data("test")["characters"]
cardSet = []
disp_card = []
cardsFPS = []

def main():
    moving = False
    create_card()

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

            for index, cardFPS in enumerate(cardsFPS):
                if event.type == cardFPS:
                    disp_card[index].cdTime()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for card in disp_card:
                    if card.rect.collidepoint(event.pos) and card.index == 9:
                        moving = True
                        tmpCard = TmpCard(card.animal, event.pos)
                        break

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if moving:
                    x, y = event.pos
                    if (x >= 139) and (x <= 139 + 892.2375) and (y >= 100) and (y <= 100 + 623.6815):
                        x, y = pos2coord(event.pos)
                        if not coordinate[x][y]:
                            create_hero(tmpCard.animal, x, y)
                            for index, card in enumerate(disp_card):
                                if card.animal == tmpCard.animal:
                                    disp_card.pop(index)
                                    cardsFPS.pop(index)
                    moving = False

            for index, ruleFPS in enumerate(enemiesFPS):
                if event.type == ruleFPS:
                    enemies.sprites()[index].hp -= 1
                    enemies.sprites()[index].animation("Run")

            for index, ruleFPS in enumerate(enemies_attackFPS):
                if event.type == ruleFPS:
                    enemies.sprites()[index].hp -= 1
                    enemies.sprites()[index].animation("Attack")

        # guidance_block.update()
        bullet_update()
        enemy_bullet_update()
        card_update()
        heroes.draw(screen)
        heroesBullet.draw(screen)
        enemies.draw(screen)
        enemies_bullet.draw(screen)

        if moving:
            tmpCard.rect.center = pygame.mouse.get_pos()  # 更新圆心位置为鼠标当前位置
            screen.blit(tmpCard.image, tmpCard.rect)

        for index, rule in enumerate(heroes.sprites()):
            if rule.isDead and (len(rule.characterAnimation) == 1 or rule.index == (
                    rule.characterAnimation[1][1] - rule.characterAnimation[1][0])):
                rule.kill()
                coordinate[rule.coord[0]][rule.coord[1]] = 0
                heroesFPS.remove(heroesFPS[index])

        for index, rule in enumerate(enemies.sprites()):
            if rule.is_dead:
                enemies.remove(rule)
                enemiesFPS.remove(enemiesFPS[index])
                enemies_attackFPS.remove(enemies_attackFPS[index])
                rule.kill()

        cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
        screen.blit(cursor_surface, cursor_rect)  # draw the cursor
        pygame.display.update()
        clock.tick(90)

if __name__ == "__main__":
    main()