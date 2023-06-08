import time
from dataDB import *
import pygame, sys, cv2
from play_sound import *

user = "test_level1"
level = "INFIN."

game_state = "login"
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
    def __init__(self, file, pos, state=False):
        self.image = pygame.image.load(f"image/home_page/{file}.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.state = state

class Level_btn(Btn):
    def __init__(self, file, pos, available, level, state=False):
        super().__init__(file, pos, state)
        self.available = available
        self.level = level

def auto_login():
    with open('local_data.json') as f:
        data = json.load(f)
        pw = data["pw"]
        account = data["account"]

        info = get_data(account)
        if info:
            print(f"Auto logining-> Account:{account}")
            if info["pw"] == pw:
                print(f"{account} logged in successfully")
                global user
                user = account
                return "home"
            else:
                print(f"Wrong password with account: {account}")
                return "login"
        else:
            print(f"Login failed with account: {account}")
            return "login"

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

    account_entry_btn = Btn("entry_off", (740, 280))
    pw_entry_btn = Btn("entry_off", (740, 360))

    while True:
        name_text = Text(name, (750, 282), 40, black)
        pw_text = Text(" *"*len(pw), (745, 367), 20, black)
        screen.blit(water_bg.image, water_bg.rect)
        screen.blit(home_bg, (0, 0))
        screen.blit(play.image, play.rect)
        screen.blit(login_bg, (0, 0))
        screen.blit(login_btn.image, login_btn.rect)
        screen.blit(create_btn.image, create_btn.rect)
        screen.blit(account_entry_btn.image, account_entry_btn.rect)
        screen.blit(pw_entry_btn.image, pw_entry_btn.rect)
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
                play_sound("click_sound") #click sound effect
                if login_btn.rect.collidepoint(event.pos):
                    login_btn.state = True
                    enter_state = "name"
                if create_btn.rect.collidepoint(event.pos):
                    create_btn.state = True
                    enter_state = "name"
                if account_entry_btn.rect.collidepoint(event.pos):
                    account_entry_btn.state = True

                if pw_entry_btn.rect.collidepoint(event.pos):
                    pw_entry_btn.state = True

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if account_entry_btn.state:
                    enter_state = "name"
                    account_entry_btn.state = False

                if pw_entry_btn.state:
                    enter_state = "pw"
                    pw_entry_btn.state = False

                if login_btn.state:
                    login_btn.state = False
                    info = get_data(name)
                    if info:
                        if info["pw"] == pw:
                            print(f"{name} logged in successfully")

                            global user
                            #change json account and password to the correct one
                            with open('local_data.json') as f:
                                data = json.load(f)
                                data["pw"] = pw
                                data["account"] = name

                                with open("local_data.json", "w", encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, sort_keys=True,
                                            ensure_ascii=False)

                            user = name
                            return "home"
                        else:
                            name = ""
                            pw = ""
                    else:
                        name = ""
                        pw = ""
                if create_btn.state:
                    create_btn.state = False
                    if not get_data(name) and name and pw:
                        from datetime import datetime
                        data = {"account": name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "pw": pw, "coin": 50, "characters": "cat,bee,mushroom,bird", "level": 1, "infinite_score":0, "last_use_mouse":1}
                        insert_data(data)
                        user = name

                        #update json file
                        with open('local_data.json') as f:
                            data = json.load(f)
                            data["account"] = name
                            data["pw"] = pw

                            with open("local_data.json", "w", encoding='utf-8') as f:
                                        json.dump(data, f, indent=2, sort_keys=True,
                                                ensure_ascii=False)
                        return "home"
                    else:
                        name = ""
                        pw = ""

            if enter_state == "name":
                account_entry_btn = Btn("entry_on", (740, 280), account_entry_btn.state)
                pw_entry_btn = Btn("entry_off", (740, 360), pw_entry_btn.state)
            else:
                account_entry_btn = Btn("entry_off", (740, 280), account_entry_btn.state)
                pw_entry_btn = Btn("entry_on", (740, 360), pw_entry_btn.state)

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

            if event.type == pygame.KEYDOWN:
                if enter_state == "name" and len(name) <= 12:
                    if event.key == pygame.K_RETURN:
                        enter_state = "pw"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                        # print(name)
                if enter_state == "pw" and len(pw) <= 20:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        pw = pw[:-2]
                    else:
                        pw += event.unicode

            pygame.display.update()
            clock.tick(200)
def home():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("EGG DEFENSE")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    play_sound("home_bgm", loop=True) #play bgm
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
    exit_btn = Btn("exit", (1185, 52))
    welcome = Btn("welcome", (195, 50))
    welcome_text = Text(f"Hi, {user}!", (195, 48), 40, (80, 80, 80))

    while True:
        screen.blit(water_bg.image, water_bg.rect)
        screen.blit(home_bg, (0, 0))
        screen.blit(play.image, play.rect)
        screen.blit(exit_btn.image, exit_btn.rect)
        screen.blit(welcome.image, welcome.rect)
        screen.blit(welcome_text.text, welcome_text.rect)

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
                if exit_btn.rect.collidepoint(event.pos):
                    exit_btn.state = True

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if play.state:
                    play_sound("click_sound") #click sound effect
                    time.sleep(0.4) #this delay is for playing the sound
                    play.state = False
                    pygame.quit()
                    return "level_choice"
                elif exit_btn.state:
                    play_sound("click_sound") #click sound effect
                    time.sleep(0.4) #this delay is for playing the sound
                    # if log out then clear the json file's account and pw
                    with open('local_data.json') as f:
                        data = json.load(f)
                        data["pw"] = "None"
                        data["account"] = "None"

                        with open("local_data.json", "w", encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, sort_keys=True,
                                            ensure_ascii=False)
                    return "login"

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

            pygame.display.update()
            clock.tick(90)

def level_choice():
    from dataDB import get_data
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("EGG DEFENSE")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    play_sound("level_bgm", loop=True) #play the bgm

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
    level_bg = pygame.image.load("image/home_page/level_choice.png").convert_alpha()
    water_bg = Water()
    pygame.time.set_timer(pygame.USEREVENT, water_bg.fps)
    play = Btn("play", (1020, 500))
    level_btn = []
    level_text = []
    level_num = get_data(user)["level"]
    for i in range(1, 4):
        if level_num >= i:
            level_btn.append(Level_btn("level_btn", (410+227*(i-1), 295), True, i))
            level_text.append(Btn(f"level{i}_text", (412+227*(i-1), 285)))
        else:
            level_btn.append(Level_btn("level_btn", (410+227*(i-1), 295), False, i))
            level_text.append(Btn("lock", (412 + 227 * (i - 1), 285)))
    infin_btn = Btn("infin_btn", (640, 485))

    while True:
        screen.blit(water_bg.image, water_bg.rect)
        screen.blit(home_bg, (0, 0))
        screen.blit(play.image, play.rect)
        screen.blit(level_bg, (0, 0))
        screen.blit(infin_btn.image, infin_btn.rect)
        for btn in level_btn:
            screen.blit(btn.image, btn.rect)
            # print(btn.available)
        for text in level_text:
            screen.blit(text.image, text.rect)

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
                play_sound("click_sound")
                for i in range(len(level_btn)):
                    if level_btn[i].rect.collidepoint(event.pos) and level_btn[i].available:
                        level_btn[i].state = True
                if infin_btn.rect.collidepoint(event.pos):
                    infin_btn.state = True

            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                global level
                for i in range(len(level_btn)):
                    if level_btn[i].state:
                        level_btn[i].state = False
                        level = i+1
                        return "main"
                if infin_btn.state:
                    level = "INFIN."
                    return "main"

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

            pygame.display.update()
            clock.tick(200)

if __name__ == "__main__":
    game_state = auto_login()
    while True:
        
        if game_state == "login":
            game_state = login()
        if game_state == "home":
            pygame.quit()
            game_state = home()
        if game_state == "level_choice":
            game_state = level_choice()
        if game_state == "main":
            from main import main
            play_time, game_state, use_mouse = main(game_state, user, level)
        if game_state == "game_over_lose":
            from game_over import lose
            game_state = lose(use_mouse=use_mouse)
        if game_state == "game_over_win":
            from game_over import win
            game_state = win(use_mouse=use_mouse, level=level, user=user)
        if game_state == "game_over_infin":
            from game_over import infin
            game_state = infin(use_mouse=use_mouse, user=user, play_time=play_time)