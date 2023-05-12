import pygame, sys

pygame.init()

# 設定視窗
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sean's game")
bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))

clock = pygame.time.Clock()  # 建立時間元件
surf = pygame.image.load(f'image/enemy/crabby/02-Run/Run 01.png').convert_alpha()

rect = surf.get_rect(center=(100, 100))

# 關閉程式的程式碼
running = True
while running:
    clock.tick(90)  # 每秒執行30次
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg, (0, 0))  # 重繪視窗
    screen.blit(surf, rect)
    pygame.display.update()  # 更新視窗

pygame.quit()