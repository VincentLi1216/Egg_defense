import pygame
import sys
import cv2
from main import distance


class Bg:
    def __init__(self):
        self.pos = (screen.get_size()[0]/2, screen.get_size()[1]/2-70)
        self.surface = [pygame.image.load(
            f"image/game_over/lose_bg/lose_bg{i}.png").convert_alpha() for i in range(2)]
        self.index = 0
        self.rect = self.surface[0].get_rect(center=self.pos)
        self.fps_counter = pygame.USEREVENT + 1
        self.fps = 50

    def animation(self):
        self.index = 0 if self.index else 1


class Text:
    def __init__(self, text, pos, size, color):
        font = pygame.font.Font('fonts/void_pixel-7.ttf', size)
        self.text = font.render(text, False, color)
        self.rect = self.text.get_rect(center=pos)


class Egg:
    def __init__(self):
        self.pos = (screen.get_size()[0]/2, screen.get_size()[1]/2-70)
        self.image = pygame.image.load(
            f"image/game_over/egg0.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.move = -1
        self.fps_counter = pygame.USEREVENT
        self.fps = 15

    def animation(self):
        if self.rect.centery <= self.pos[1] - 50:
            self.move = 1
        elif self.rect.centery >= self.pos[1]:
            self.move = -1
        self.rect.centery += self.move


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("EGG DEFENSE")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
# over_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
# over_bg.fill((255, 255, 255, 255))
lose_bg = Bg()

cursor_surface = [pygame.image.load("image/cursor/cursor.png").convert_alpha(
), pygame.image.load("image/cursor/grab_cursor.png").convert_alpha()]
cursor_surface = [pygame.transform.scale(
    cursor_surface[0], (70, 70)), pygame.transform.scale(cursor_surface[1], (70, 70))]
cursor_rect = cursor_surface[0].get_rect()

black = (0, 0, 0)


def game_over(use_mouse):
    from main import cursor_grabbed, x4, y4, cap, mp_hands, mp_drawing, mp_drawing_styles, mouse_down
    egg = Egg()
    game_over_text = Text("YOU LOSE", (screen.get_size()[
                          0]/2, screen.get_size()[1]/2+120), 180, black)
    pygame.time.set_timer(pygame.USEREVENT, egg.fps)

    trans_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    trans_alpha = 255

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
