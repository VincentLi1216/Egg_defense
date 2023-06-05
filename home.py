import time
from dataDB import *
import pygame, sys, cv2
from play_sound import *

user = "test_level3"
level = "INFIN."

game_state = "home"
use_mouse = True

class Water:
    def __init__(self):
        self.image = pygame.image.load("image/home_page/water.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.moving = -8
        self.fps = 500
        self.fps_counter = pygame.USEREVENT

    def animation(self):
        self.rect.centerx += self.moving
        self.moving *= (-1)

class Text:
    def __init__(self, text, pos, size, color):
        font = pygame.font.Font('fonts/Cubic_11_1.013_R.ttf', size)
        self.text = font.render(text, False, color)
        self.rect = self.text.get_rect(center=pos)

class Btn:
    def __init__(self, file, pos):
        self.image = pygame.image.load(f"image/home_page/{file}.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.state = False

def login():
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
    mouse_down = False
    cursor_grabbed = False

    use_mouse = True
    home_bg = pygame.image.load("image/home_page/home.png").convert_alpha()
    login_bg = pygame.image.load("image/home_page/login.png").convert_alpha()
    water_bg = Water()
    pygame.time.set_timer(pygame.USEREVENT, water_bg.fps)
    play = Btn("play", (1020, 500))
    login_btn = Btn("login_btn", (490, 470))
    create_btn = Btn("create_btn", (800, 470))

    enter_state = "name"
    name = ""
    pw = ""
    name_text = Text(name, (750, 285), 40, black)
    pw_text = Text(pw, (745, 370), 20, black)
    type_time = time.time()

    while True:
        screen.blit(water_bg.image, water_bg.rect)
        screen.blit(home_bg, (0, 0))
        screen.blit(play.image, play.rect)
        screen.blit(login_bg, (0, 0))
        screen.blit(login_btn.image, login_btn.rect)
        screen.blit(create_btn.image, create_btn.rect)
        screen.blit(name_text.text, name_text.rect)
        screen.blit(pw_text.text, pw_text.rect)

        for event in pygame.event.get():

            if event.type == water_bg.fps_counter:
                water_bg.animation()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                cursor_grabbed = True

            else:
                if use_mouse and mouse_down and event.type == pygame.MOUSEBUTTONUP:
                    cursor_grabbed = False
                    mouse_down = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_btn.rect.collidepoint(event.pos):
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    login_btn.state = True
                if create_btn.rect.collidepoint(event.pos):
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    create_btn.state = True

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if login_btn.state:
                    login_btn.state = False
                    info = get_data(name)
                    if info:
                        print(name, pw)
                        if info["pw"] == pw:
                            print(f"{name} logged in successfully")
                            global user
                            user = name
                            return "home"
                        else:
                            name = ""
                            pw = ""
                    else:
                        name = ""
                        pw = ""
                if create_btn.state:
                    if not get_data(name) and name and pw:
                        from datetime import datetime
                        data = {"account": name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "pw": pw, "coin": 50, "characters": "cat,bee,mushroom,bird", "level": 1}
                        insert_data(data)
                        user = name
                        return "home"
                    else:
                        name = ""
                        pw = ""

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

            char = ""
            if pygame.key.get_pressed()[pygame.K_0]:
                char = "0" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_1]:
                char = "1" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_2]:
                char = "2" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_3]:
                char = "3" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_4]:
                char = "4" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_5]:
                char = "5" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_6]:
                char = "6" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_7]:
                char = "7" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_8]:
                char = "8" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_9]:
                char = "9" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_a]:
                char = "a" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_b]:
                char = "b" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_c]:
                char = "c" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_d]:
                char = "d" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_e]:
                char = "e" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_f]:
                char = "f" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_g]:
                char = "g" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_h]:
                char = "h" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_i]:
                char = "i" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_j]:
                char = "j" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_k]:
                char = "k" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_l]:
                char = "l" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_m]:
                char = "m" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_n]:
                char = "n" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_o]:
                char = "o" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_p]:
                char = "p" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_q]:
                char = "q" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_r]:
                char = "r" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_s]:
                char = "s" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_t]:
                char = "t" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_u]:
                char = "u" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_v]:
                char = "v" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_w]:
                char = "w" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_x]:
                char = "x" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_y]:
                char = "y" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_z]:
                char = "z" if time.time() - type_time >= 0.05 else char
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                if time.time() - type_time >= 0.05:
                    enter_state = "pw"
                    char = ""
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                if time.time() - type_time >= 0.05:
                    name = name[:-1] if enter_state == "name" else name
                    pw = pw[:-1] if enter_state == "pw" else pw
                    name_text = Text(name, (750, 285), 40, black)
                    pw_text = Text(" *" * len(pw), (745, 370), 20, black)
                    type_time = time.time()
                char = ""
            if time.time() - type_time >= 0.05:
                name = name + char if enter_state == "name" else name
                pw = pw + char if enter_state == "pw" else pw
                name_text = Text(name, (750, 285), 40, black)
                pw_text = Text(" *"*len(pw), (745, 370), 20, black)
                type_time = time.time()

            pygame.display.update()
            clock.tick(90)
def home():
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
    mouse_down = False
    cursor_grabbed = False

    use_mouse = True
    home_bg = pygame.image.load("image/home_page/home.png").convert_alpha()
    water_bg = Water()
    pygame.time.set_timer(pygame.USEREVENT, water_bg.fps)
    play = Btn("play", (1020, 500))

    while True:
        screen.blit(water_bg.image, water_bg.rect)
        screen.blit(home_bg, (0, 0))
        screen.blit(play.image, play.rect)

        for event in pygame.event.get():

            if event.type == water_bg.fps_counter:
                water_bg.animation()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                cursor_grabbed = True

            else:
                if use_mouse and mouse_down and event.type == pygame.MOUSEBUTTONUP:
                    cursor_grabbed = False
                    mouse_down = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.rect.collidepoint(event.pos):
                    play.state = True

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if play.state:
                    play_sound("sound_effects/click_sound.mp3") #click sound effect
                    time.sleep(0.4) #this delay is for playing the sound
                    play.state = False
                    pygame.quit()
                    return "main"

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

            pygame.display.update()
            clock.tick(90)

if __name__ == "__main__":
    game_state = login()
    # game_state = "main"
    while True:
        if game_state == "home":
            pygame.quit()
            game_state = home()
        if game_state == "main":
            from main import main
            game_state, use_mouse = main(game_state, user, level)
        if game_state == "game_over_lose":
            from game_over import lose
            game_state = lose(use_mouse=use_mouse)
        if game_state == "game_over_win":
            from game_over import win
            game_state = win(use_mouse=use_mouse, level=level, user=user)