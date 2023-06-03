import pygame, sys, cv2

user = "test_level1"
level = 1

game_state = "main"
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

    name_text = Text("", (750, 285), 40, black)
    pw_text = Text("", (745, 370), 20, black)

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

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if play.rect.collidepoint(event.pos):
            #         play.state = True
            #
            # if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
            #     if play.state:
            #         play.state = False
            #         pygame.quit()
            #         return "main"

            cursor_rect.center = pygame.mouse.get_pos()  # update cursor position
            if cursor_grabbed:
                # draw the cursor
                screen.blit(cursor_surface[1], cursor_rect)
            else:
                # draw the cursor
                screen.blit(cursor_surface[0], cursor_rect)

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
    # login()
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