import cv2
import math
import mediapipe as mp
from dataDB import get_data
import pygame
import sys
import random
import os
import copy
import time
from character_dict import *
from hand_detection import *
from level_design import *
use_mouse = True
level = 1


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
            self.surface = [pygame.image.load(
                f"image/{side}/{self.name}/{surface[0]}_{self.name}.png").convert_alpha()]
        else:
            self.surface = [pygame.image.load(
                f"image/{side}/{self.name}/{surface[0]}_{self.name}{index}.png").convert_alpha()]
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
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"], (
            self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
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
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"], (
            self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

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
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

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
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)


class rhino(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 5)]
        self.animal = "rhino"
        self.isDead = False
        self.speed = 8
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

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
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
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
        while heroes.sprites()[target].animal == "cat":
            target += 1
            if target == len(heroes.sprites()):
                target = -1
                break
        if target != -1:
            for index in range(target, len(heroes.sprites())):
                if (heroesInfo[heroes.sprites()[index].animal]["hp"] - heroes.sprites()[index].hp) > \
                        (heroesInfo[heroes.sprites()[target].animal]["hp"] - heroes.sprites()[target].hp) and heroes.sprites()[index].animal != "cat":
                    target = index
            heroes.sprites()[target].hp = heroes.sprites()[target].hp + 5 if heroes.sprites()[target].hp < heroesInfo[
                heroes.sprites()[target].animal]["hp"] else heroes.sprites()[target].hp


class Fox(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 10), (11, 17)]
        self.animal = "fox"
        self.isDead = False
        self.load_dead = False
        fps = 100
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
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
        for enemy in enemies.sprites():
            enemy.speed = -3
            enemy.attack_moving_speed = -3


class Turtle(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 15), (16, 19)]
        self.animal = "turtle"
        self.isDead = False
        self.load_dead = False
        self.speed_x = 7
        self.speed_y = 0
        fps = 100
        super().__init__(heroesInfo[self.animal]["hp"], (pos[0], pos[1]-25), heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
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
        fps = 100
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

    def animation(self):
        if self.hp > 0:
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
        else:
            if not self.load_dead:
                self.surface = [
                    pygame.image.load(
                        f"image/{self.characterSide}/{self.animal}/{self.animal}{i}.png").convert_alpha()
                    for i in range(self.characterAnimation[1][0], self.characterAnimation[1][1] + 1)]
                self.load_dead = True
                self.index = 0
            if self.index == (self.characterAnimation[1][1] - self.characterAnimation[1][0]):
                pass
            else:
                self.index += 1
        self.image = self.surface[self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)
        for enemy in enemies.sprites():
            if 50 <= enemy.rect.centery - self.rect.centery <= 150:
                if 140 <= enemy.rect.centerx - self.rect.centerx <= 200:
                    self.skill(2)
            elif -50 <= enemy.rect.midbottom[1] - self.rect.midbottom[1] <= 50:
                if enemy.rect.centerx - self.rect.centerx > 0:
                    self.skill(1)
            elif -150 <= enemy.rect.centery - self.rect.centery <= -50:
                if 140 <= enemy.rect.centerx - self.rect.centerx <= 200:
                    self.skill(0)

    def skill(self, direction):
        self.round = self.index
        if self.index == (len(self.surface) // 2):
            heroesBullet.add(
                Bullet(self.rect, (self.animal, 3), self.characterSide, self.damage, heroesInfo[self.animal]["speed_x"], heroesInfo[self.animal]["speed_y"][direction], direction))


class Turkey(Hero):
    def __init__(self, pos):
        self.characterAnimation = [(0, 13), (14, 19)]
        self.animal = "turkey"
        self.isDead = False
        self.load_dead = False
        self.speed = 10
        fps = 10
        super().__init__(heroesInfo[self.animal]["hp"], pos, heroesInfo[self.animal]["damage"],
                         (self.animal, self.characterAnimation[0][1]), heroesInfo[self.animal]["fps"])

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
    def __init__(self, name, pos):

        self.name = name
        self.characterSide = "enemy"
        self.show_mode = "Run"
        for attribute in ["hp", "damage", "fps", "speed", "attack_fps", "attack_moving_speed"]:
            self.__dict__[attribute] = enemiesInfo[name][str(attribute)]
        self.is_dead = False
        self.is_dead_load = False
        self.mode_change_enable = True
        self.indexes_show_after_dead = 10
        self.has_attacked = False
        self.isDead = False  # just for testing
        self.surfaces = {}
        all_mode = ["Run", "Attack", "Hit", "Dead"]
        super().__init__(hp=self.hp, pos=pos, damage=self.damage, fps=self.fps)

        for i, mode in enumerate(all_mode):
            project_dir = f"image/{self.characterSide}/{self.name}/{mode}"
            file_count = 0
            for folder, _, filenames in os.walk(project_dir):
                for filename in filenames:
                    if filename.endswith(".png"):
                        file_count += 1
            self.surfaces[mode] = [pygame.image.load(
                f'{project_dir}/{j + 1}.png').convert_alpha() for j in range(file_count)]
        self.image = self.surfaces[self.show_mode][self.index]
        self.rect = self.image.get_rect(midbottom=self.pos)

    # for the animation of the character
    def animation(self, mode, attack_moving_speed, has_bullet=False):
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
        super().__init__(name, pos)

    def animation(self, mode):
        super().animation(mode, self.attack_moving_speed)
        # brighten = 128
        # self.surfaces["Run"][0].fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)


class Fierce_Tooth(Enemy):
    def __init__(self, pos):
        name = "Fierce Tooth"
        super().__init__(name, pos)

    def animation(self, mode):
        super().animation(mode, self.attack_moving_speed)


class Pink_Star(Enemy):
    def __init__(self, pos):
        name = "Pink Star"
        super().__init__(name, pos)

    def animation(self, mode):
        super().animation(mode, self.attack_moving_speed)


class Seashell(Enemy):
    def __init__(self, pos):
        name = "Seashell"
        self.bullet_speed = -8
        super().__init__(name, pos)

    def animation(self, mode):
        super().animation(mode, self.attack_moving_speed, has_bullet=True)


class Whale(Enemy):
    def __init__(self, pos):
        name = "Whale"
        super().__init__(name, pos)

    def animation(self, mode):
        super().animation(mode, self.attack_moving_speed)


class Card:
    def __init__(self, animal):
        self.animal = animal
        self.surface = [pygame.image.load(
            f"image/card/card_{self.animal}{i}.png").convert_alpha() for i in range(10)]
        self.rect = self.surface[0].get_rect(topleft=(0, 12.4222))
        self.image = self.surface[0]
        self.index = 0
        self.fps = heroesInfo[self.animal]["cardCD"]

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
        self.image = pygame.image.load(
            f"image/hero/{self.animal}/{self.animal}0.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

# class Guidance_block:
#     def __init__(self):
#         self.image = pygame.Surface((148.5726, 124.7363), pygame.SRCALPHA)
#         self.image.fill((255, 255, 255, 128))
#         self.rect = self.image.get_rect()
#     def update(self):
#         x, y = pygame.mouse.get_pos()
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
        heroes.add(
            Mushroom((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
        coordinate[x][y] = 1
    elif animal == 'rhino':
        heroes.add(rhino((211.2731 + 148.5726 * y, 222.3947 + 124.7363 * x - 3)))
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
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter,
                          heroes.sprites()[-1].fps)
    FPSCounter += 1


def bullet_update():
    global FPSCounter
    for rule in heroes.sprites():
        if rule.animal in ("dog", "bird", "frog") and (rule.round != rule.index):
            rule.round = rule.index
            if rule.index == (len(rule.surface)//2):
                heroesBullet.add(
                    Bullet(rule.rect, (rule.animal, 3), rule.characterSide, rule.damage, heroesInfo[rule.animal]["speed_x"], heroesInfo[rule.animal]["speed_y"]))

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
            enemies_bullet.add(Enemy_bullet(
                rule.rect, "image/enemy/Pearl/Idle/1.png", rule.damage, rule.bullet_speed))
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

    global FPSCounter
    enemiesFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter,
                          enemies.sprites()[-1].fps)
    FPSCounter += 1
    enemies_attackFPS.append(pygame.USEREVENT + FPSCounter)
    pygame.time.set_timer(pygame.USEREVENT + FPSCounter,
                          enemies.sprites()[-1].attack_fps)
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
                    pygame.time.set_timer(
                        pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
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
                    pygame.time.set_timer(
                        pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
                    FPSCounter += 1
                    break
            else:
                animal = random.choice(playerCard)
                disp_card.append(Card(animal))

                cardsFPS.append(pygame.USEREVENT + FPSCounter)
                pygame.time.set_timer(
                    pygame.USEREVENT + FPSCounter, disp_card[-1].fps)
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
cursor_surface = [pygame.image.load("image/cursor/cursor.png").convert_alpha(
), pygame.image.load("image/cursor/grab_cursor.png").convert_alpha()]
cursor_surface = [pygame.transform.scale(
    cursor_surface[0], (70, 70)), pygame.transform.scale(cursor_surface[1], (70, 70))]
cursor_rect = cursor_surface[0].get_rect()

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


playerCard = get_data("test_new")["characters"]
# playerCard = ["cat", 'turtle', "fox", "bee", "mushroom"]
cardSet = []
disp_card = []
cardsFPS = []
game_design = copy.deepcopy(level_design)


def heroes_skill_collisions():
    collisions = pygame.sprite.groupcollide(heroes, enemies, False, False)
    for hero in collisions:
        heroes_attack = collisions[hero]
        for enemy in heroes_attack:
            if hero.animal in ("rhino", "turkey"):
                if hero.animal == "turkey" and (enemy.rect.centerx - hero.rect.centerx) <= 90:
                    enemy.hp = -1
                if hero.animal == "rhino" and -60 <= (enemy.rect.centery - hero.rect.centery) <= 60:
                    enemy.hp -= hero.damage
            if hero.animal == "turtle" and (enemy.rect.midleft[0] <= hero.rect.midright[0]-20):
                hero.hp = enemy.hp = -1


def heroes_bullet_collisions():
    collisions = pygame.sprite.groupcollide(
        heroesBullet, enemies, False, False)
    for bullet in collisions:
        heroes_attack = collisions[bullet]
        for enemy in heroes_attack:
            if enemy.rect.centerx - bullet.rect.centerx <= 20:
                enemy.hp -= bullet.damage
                bullet.kill()


def heroes2enemies_collisions():
    collisions = pygame.sprite.groupcollide(heroes, enemies, False, False)
    for hero in collisions:
        heroes_attack = collisions[hero]
        for enemy in heroes_attack:
            if (hero.rect.centerx >= enemy.rect.midleft[0]-30) and (hero.animal != "turtle") \
                    and -60 <= (enemy.rect.centery - hero.rect.centery) <= 60 and hero.rect.midright[0]+20 <= enemy.rect.midright[0]:
                hero.hp -= 0.1
                enemy.speed = 0
                enemy.attack_moving_speed = 0


def enemies2heroes_collisions():
    collisions = pygame.sprite.groupcollide(enemies, heroes, False, False)
    for enemy in collisions:
        enemies_attack = collisions[enemy]
        for hero in enemies_attack:
            if enemy.show_mode == "Attack" and enemy.index == 0 and -60 <= (enemy.rect.centery - hero.rect.centery) <= 60:
                hero.hp -= enemy.damage


def enemies_bullet_collisions():
    collisions = pygame.sprite.groupcollide(
        enemies_bullet, heroes, False, False)
    for bullet in collisions:
        enemies_attack = collisions[bullet]
        for hero in enemies_attack:
            if bullet.rect.centerx - hero.rect.centerx <= 20:
                hero.hp -= bullet.damage
                bullet.kill()


def reset_enemies_speed():
    for enemy in enemies.sprites():
        enemy.speed = enemiesInfo[enemy.name]["speed"]
        enemy.attack_moving_speed = enemiesInfo[enemy.name]["attack_moving_speed"]


mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法

cap = cv2.VideoCapture(1)


def distance(x1, y1, x2, y2):
    return math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))


def main():
    global moving
    global use_mouse
    moving = False
    hand_closed = False
    cursor_grabbed = False
    create_card()
    x4 = 0
    y4 = 0
    rm_enemy_num = 0
    begin_time = time.time()

    # mediapipe 啟用偵測手掌
    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:

            # create enemy from the dict
            for i in range(len(game_design[level])):
                if game_design[level][i]["time"] <= time.time() - begin_time:
                    # print(len(game_design[level]))
                    create_enemy(
                        game_design[level][i]["enemy"], game_design[level][i]["row"])
                    # print(game_design[level][i]["enemy"])
                    rm_enemy_num += 1

            for _ in range(rm_enemy_num):
                game_design[level].pop(0)
                # print(game_design[level])

            rm_enemy_num = 0

            ret, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1280, 720))
            size = img.shape   # 取得攝影機影像尺寸
            w = size[1]        # 取得畫面寬度
            h = size[0]        # 取得畫面高度
            if not ret:
                print("Cannot receive frame")
                break
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
            results = hands.process(img2)                 # 偵測手掌
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 將節點和骨架繪製到影像中
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    x8 = hand_landmarks.landmark[8].x * w  # 取得食指末端 x 座標
                    y8 = hand_landmarks.landmark[8].y * h  # 取得食指末端 y 座標
                    x4 = hand_landmarks.landmark[4].x * w  # 取得食指末端 x 座標
                    y4 = hand_landmarks.landmark[4].y * h  # 取得食指末端 y 座標
                    x0 = hand_landmarks.landmark[0].x * w  # 取得食指末端 x 座標
                    y0 = hand_landmarks.landmark[0].y * h  # 取得食指末端 y 座標
                    x5 = hand_landmarks.landmark[5].x * w  # 取得食指末端 x 座標
                    y5 = hand_landmarks.landmark[5].y * h  # 取得食指末端 y 座標
                    if distance(x8, y8, x4, y4)/distance(x0, y0, x5, y5) <= 0.3:
                        hand_closed = True
                        cursor_grabbed = True
                        # print(f'hand closed:{int(x4)}, {int(y4)}')
                    else:
                        hand_closed = False
                        cursor_grabbed = False
                    # print(distance(x8, y8, x4, y4)/distance(x0, y0, x5, y5))

            # cv2.imshow('Hand Detection', img)
            # if cv2.waitKey(5) == ord('q'):
            #     break    # 按下 q 鍵停止

            # main game start here
            screen.blit(bg_surface, (0, 0))

            reset_enemies_speed()
            for rule in heroes.sprites():
                if rule.hp <= 0 and (not rule.isDead):
                    rule.index = 0
                    rule.isDead = True
                if rule.animal == "cat" and rule.index == len(rule.surface)/2:
                    rule.skill()
                if rule.animal == "fox":
                    rule.skill()

            # guidance_block.update()
            bullet_update()
            enemy_bullet_update()
            card_update()

            heroes_skill_collisions()
            heroes_bullet_collisions()
            enemies_bullet_collisions()
            heroes2enemies_collisions()
            enemies2heroes_collisions()

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

                if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN) or (not use_mouse and hand_closed):
                    cursor_grabbed = True
                else:
                    cursor_grabbed = False

                if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN and not moving) or (not use_mouse and hand_closed and not moving):
                    for card in disp_card:
                        if use_mouse:
                            if card.rect.collidepoint(event.pos) and card.index == 9:
                                moving = True
                                tmpCard = TmpCard(card.animal, event.pos)
                                break
                        else:
                            if card.rect.collidepoint((round(x4), round(y4))) and card.index == 9:
                                moving = True
                                tmpCard = TmpCard(
                                    card.animal, (round(x4), round(y4)))
                                break

                if (event.type == pygame.MOUSEBUTTONUP and use_mouse) or (not use_mouse and not hand_closed):  # 获取松开鼠标事件
                    if moving:
                        if use_mouse:
                            x, y = event.pos
                        else:
                            x, y = (round(x4), round(y4))
                        if (x >= 139) and (x <= 139 + 892.2375) and (y >= 100) and (y <= 100 + 623.6815):
                            if use_mouse:
                                x, y = pos2coord(event.pos)
                            else:
                                x, y = pos2coord((round(x4), round(y4)))

                            if not coordinate[x][y]:
                                create_hero(tmpCard.animal, x, y)
                                for index, card in enumerate(disp_card):
                                    if card.animal == tmpCard.animal:
                                        disp_card.pop(index)
                                        cardsFPS.pop(index)
                        moving = False

                for index, ruleFPS in enumerate(enemiesFPS):
                    if event.type == ruleFPS:
                        # enemies.sprites()[index].hp -= 1
                        enemies.sprites()[index].animation("Run")

                for index, ruleFPS in enumerate(enemies_attackFPS):
                    if event.type == ruleFPS:
                        # enemies.sprites()[index].hp -= 1
                        enemies.sprites()[index].animation("Attack")

            enemies.draw(screen)
            enemies_bullet.draw(screen)
            heroes.draw(screen)
            heroesBullet.draw(screen)

            if moving:
                if use_mouse:
                    tmpCard.rect.center = pygame.mouse.get_pos()  # 更新圆心位置为鼠标当前位置
                else:
                    tmpCard.rect.center = (round(x4), round(y4))
                screen.blit(tmpCard.image, tmpCard.rect)

            for index, rule in enumerate(heroes.sprites()):
                if rule.isDead and (len(rule.characterAnimation) == 1 or rule.index == (
                        rule.characterAnimation[1][1] - rule.characterAnimation[1][0])):
                    rule.kill()
                    coordinate[rule.coord[0]][rule.coord[1]] = 0
                    heroesFPS.remove(heroesFPS[index])

            # reversed the list to prevent kill the two enemies at the same time
            for index, rule in list(reversed(list(enumerate(enemies.sprites())))):
                if rule.is_dead:
                    enemies.remove(rule)
                    enemiesFPS.remove(enemiesFPS[index])
                    enemies_attackFPS.remove(enemies_attackFPS[index])
                    rule.kill()

            if use_mouse:
                cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
                if cursor_grabbed:
                    # draw the cursor
                    screen.blit(cursor_surface[1], cursor_rect)
                else:
                    # draw the cursor
                    screen.blit(cursor_surface[0], cursor_rect)

            else:
                cursor_rect.center = (round(x4), round(y4))
                if cursor_grabbed:
                    # draw the cursor
                    screen.blit(cursor_surface[1], cursor_rect)
                else:
                    # draw the cursor
                    screen.blit(cursor_surface[0], cursor_rect)
                # print((round(x4), round(y4)))
            pygame.display.update()
            clock.tick(90)


if __name__ == "__main__":
    main()
