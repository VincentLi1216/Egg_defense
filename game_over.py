import pygame
import sys
import cv2
import time
from main import distance
from play_sound import *


class Bg:
    def __init__(self, file):
        self.pos = (screen.get_size()[0]/2, screen.get_size()[1]/2-70)
        self.surface = [pygame.image.load(
            f"image/game_over/{file}{i}.png").convert_alpha() for i in range(2)]
        self.index = 0
        self.rect = self.surface[0].get_rect(center=self.pos)
        self.fps_counter = pygame.USEREVENT + 1
        self.fps = 50

    def animation(self):
        self.index = 0 if self.index else 1


class Text:
    def __init__(self, text, pos, size, color):
        font = pygame.font.Font('fonts/Cubic_11_1.013_R.ttf', size)
        self.text = font.render(text, False, color)
        self.rect = self.text.get_rect(center=pos)

class Btn:
    def __init__(self, func, pos):
        self.image = pygame.image.load(
            f"image/game_over/{func}.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.state = False

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("EGG DEFENSE")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
# over_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
# over_bg.fill((255, 255, 255, 255))

cursor_surface = [pygame.image.load("image/cursor/cursor.png").convert_alpha(
), pygame.image.load("image/cursor/grab_cursor.png").convert_alpha()]
cursor_surface = [pygame.transform.scale(
    cursor_surface[0], (70, 70)), pygame.transform.scale(cursor_surface[1], (70, 70))]
cursor_rect = cursor_surface[0].get_rect()

black = (0, 0, 0)

def lose(use_mouse):
    from main import cursor_grabbed, x4, y4, cap, mp_hands, mp_drawing, mp_drawing_styles, mouse_down
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("EGG DEFENSE")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    class Egg:
        def __init__(self):
            self.pos = (screen.get_size()[0] / 2 - 300, screen.get_size()[1] / 2)
            self.image = pygame.image.load(
                f"image/game_over/egg0.png").convert_alpha()
            self.rect = self.image.get_rect(center=self.pos)
            self.move = -1
            self.fps_counter = pygame.USEREVENT
            self.fps = 15

        def animation(self):
            if self.rect.centery <= self.pos[1] - 80:
                self.move = 2
            elif self.rect.centery >= self.pos[1] + 40:
                self.move = -2
            self.rect.centery += self.move

    lose_bg = Bg("lose_bg/lose_bg")
    egg = Egg()
    game_over_text = Text("YOU LOSE", (810, 250), 110, black)
    pygame.time.set_timer(pygame.USEREVENT, egg.fps)

    trans_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    trans_alpha = 255

    restart_btn = Btn("restart", (670, 430))
    exit_btn = Btn("exit", (950, 430))

    with mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        while True:
            screen.blit(lose_bg.surface[lose_bg.index], (0, 0))
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1280, 720))
            size = img.shape  # 取得攝影機影像尺寸
            hand_closed = False
            w = size[1]  # 取得畫面寬度
            h = size[0]  # 取得畫面高度
            if not ret:
                print("Cannot receive frame")
                break
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
            results = hands.process(img2)  # 偵測手掌
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
                    if distance(x8, y8, x4, y4) / distance(x0, y0, x5, y5) <= 0.3:
                        hand_closed = True
                        if not use_mouse:
                            cursor_grabbed = True
                    else:
                        hand_closed = False
                        if not use_mouse:
                            cursor_grabbed = False

            for event in pygame.event.get():

                if event.type == egg.fps_counter:
                    egg.animation()

                if event.type == lose_bg.fps_counter:
                    lose_bg.animation()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN) or (not use_mouse and hand_closed):
                    if use_mouse:
                        mouse_down = True
                    cursor_grabbed = True

                else:
                    if not use_mouse:
                        cursor_grabbed = False
                    elif use_mouse and mouse_down and event.type == pygame.MOUSEBUTTONUP:
                        cursor_grabbed = False
                        mouse_down = False

            screen.blit(egg.image, egg.rect)
            screen.blit(game_over_text.text, game_over_text.rect)
            screen.blit(exit_btn.image, exit_btn.rect)
            screen.blit(restart_btn.image, restart_btn.rect)

            if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN) or (
                    not use_mouse and hand_closed):
                if use_mouse:
                    if exit_btn.rect.collidepoint(event.pos):
                        exit_btn.state = True
                    elif restart_btn.rect.collidepoint(event.pos):
                        restart_btn.state = True

                else:
                    if exit_btn.rect.collidepoint((round(x4), round(y4))):
                        exit_btn.state = True
                    elif restart_btn.rect.collidepoint((round(x4), round(y4))):
                        restart_btn.state = True

            if (event.type == pygame.MOUSEBUTTONUP and use_mouse) or (
                    not use_mouse and not hand_closed):  # 获取松开鼠标事件
                if exit_btn.state:
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    time.sleep(0.4) #delay for playing the sound effect
                    return "home"








                if restart_btn.state:
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    return "main"

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

            if trans_alpha >= 0:
                trans_bg.fill((0, 0, 0, trans_alpha))
                screen.blit(trans_bg, (0, 0))
                trans_alpha -= 5

            pygame.display.update()
            clock.tick(90)

def win(use_mouse, level, user):
    import time
    from datetime import datetime
    from main import cursor_grabbed, x4, y4, cap, mp_hands, mp_drawing, mp_drawing_styles, mouse_down
    from dataDB import get_data, update_one_data

    pygame.init()
    global screen, clock
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("EGG DEFENSE")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    new_card = {1: ["dog", "fox", "frog"], 2: ["turkey", "turtle", "rhino"]}
    db_card = {1: "cat,bee,mushroom,bird,dog,fox,frog",
               2: "cat,bee,mushroom,bird,dog,fox,frog,rhino,turkey,turtle"}
    if get_data(user)["level"] == level:
        next_level = level+1 if level < 3 else level
        if level < 3:
            update_one_data("characters", db_card[level], user)
            update_one_data("level", next_level, user)

    class Chick:
        def __init__(self):
            self.characterAnimation = [(0, 5)]
            self.pos = (290, 210)
            self.surface = [pygame.image.load(f"image/game_over/win_chick/chick{i}.png").convert_alpha() for i in range(6)]
            self.image = self.surface[0]
            self.rect = self.image.get_rect(center=self.pos)
            self.index = 0
            self.fps_counter = pygame.USEREVENT
            self.fps = 100

        def animation(self):
            if self.index == (self.characterAnimation[0][1]):
                self.index = 0
            else:
                self.index += 1
            self.image = self.surface[self.index]
            self.rect = self.image.get_rect(center=self.pos)

    class Card:
        def __init__(self, animal, pos):
            self.pos = pos
            self.image = pygame.image.load(
                f"image/game_over/card/{animal}.png").convert_alpha()
            self.image = pygame.transform.scale2x(self.image)
            self.rect = self.image.get_rect(center=self.pos)

    lose_bg = Bg("win_bg/win_bg")
    chick = Chick()
    pygame.time.set_timer(pygame.USEREVENT, chick.fps)

    trans_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    trans_alpha = 255

    home_btn = Btn("home", (290, 340))
    begin_time = time.time()
    if level < 3:
        card1 = Card(new_card[level][0], (680, 600))
        card2 = Card(new_card[level][1], (880, 600))
        card3 = Card(new_card[level][2], (1080, 600))
        new_card_img = Btn("card_txt", (360, 600))
    else:
        congratulate_text = Btn("finish", (650, 600))

    with mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        while True:
            screen.blit(lose_bg.surface[lose_bg.index], (0, 0))
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1280, 720))
            size = img.shape  # 取得攝影機影像尺寸
            hand_closed = False
            w = size[1]  # 取得畫面寬度
            h = size[0]  # 取得畫面高度
            if not ret:
                print("Cannot receive frame")
                break
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
            results = hands.process(img2)  # 偵測手掌
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
                    if distance(x8, y8, x4, y4) / distance(x0, y0, x5, y5) <= 0.3:
                        hand_closed = True
                        if not use_mouse:
                            cursor_grabbed = True
                    else:
                        hand_closed = False
                        if not use_mouse:
                            cursor_grabbed = False

            for event in pygame.event.get():

                if event.type == chick.fps_counter:
                    chick.animation()

                if event.type == lose_bg.fps_counter:
                    lose_bg.animation()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN) or (not use_mouse and hand_closed):
                    if use_mouse:
                        mouse_down = True
                    cursor_grabbed = True

                else:
                    if not use_mouse:
                        cursor_grabbed = False
                    elif use_mouse and mouse_down and event.type == pygame.MOUSEBUTTONUP:
                        cursor_grabbed = False
                        mouse_down = False

            screen.blit(chick.image, chick.rect)
            screen.blit(home_btn.image, home_btn.rect)



            if level < 3:
                if time.time() - begin_time >= 3:
                    screen.blit(card1.image, card1.rect)
                    screen.blit(card2.image, card2.rect)
                    screen.blit(card3.image, card3.rect)
                elif time.time() - begin_time >= 2.5:
                    screen.blit(card1.image, card1.rect)
                    screen.blit(card2.image, card2.rect)
                elif time.time() - begin_time >= 2:
                    screen.blit(card1.image, card1.rect)
                screen.blit(new_card_img.image, new_card_img.rect)
            else:
                screen.blit(congratulate_text.image, congratulate_text.rect)

            if (use_mouse and event.type == pygame.MOUSEBUTTONDOWN) or (
                    not use_mouse and hand_closed):
                if use_mouse:
                    if home_btn.rect.collidepoint(event.pos):
                        home_btn.state = True

                else:
                    if home_btn.rect.collidepoint((round(x4), round(y4))):
                        home_btn.state = True

            if (event.type == pygame.MOUSEBUTTONUP and use_mouse) or (
                    not use_mouse and not hand_closed):  # 获取松开鼠标事件
                if home_btn.state:
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    time.sleep(0.4) #delay for playing the sound effect
                    pygame.quit()
                    return "home"

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

            if trans_alpha >= 0:
                trans_bg.fill((0, 0, 0, trans_alpha))
                screen.blit(trans_bg, (0, 0))
                trans_alpha -= 5

            pygame.display.update()
            clock.tick(90)

def infin(use_mouse, level, user):
    pass