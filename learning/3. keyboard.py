import sys

import pygame

FPS = 60
W = 800  # ширина экрана
H = 500  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
MOVE_DELTA = 3

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# координаты и радиус круга
x = W // 2
y = H // 2
r = 50


while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)
    pygame.draw.circle(sc, BLUE, (x, y), r)
    pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        pass
    elif keys[pygame.K_LEFT]:
        x -= MOVE_DELTA
    elif keys[pygame.K_RIGHT]:
        x += MOVE_DELTA
    elif x < W // 2:
        x += MOVE_DELTA
    elif x > W // 2:
        x -= MOVE_DELTA

    if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
        pass
    elif keys[pygame.K_UP]:
        y -= MOVE_DELTA
    elif keys[pygame.K_DOWN]:
        y += MOVE_DELTA
    elif y < H // 2:
        y += MOVE_DELTA
    elif y > H // 2:
        y -= MOVE_DELTA

    clock.tick(FPS)
