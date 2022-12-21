import sys

import pygame as pg

FPS = 60
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)

LEFT = 0
MIDDLE = 1
RIGHT = 2


def main():
    sc = pg.display.set_mode((800, 500))
    sc.fill(WHITE)
    pg.display.update()
    clock = pg.time.Clock()

    while True:
        clock.tick(FPS)
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()

            mouse_pressed = pg.mouse.get_pressed()
            mouse_position = pg.mouse.get_pos()
            need_update = False
            if mouse_pressed[LEFT]:
                pg.draw.circle(sc, RED, mouse_position, 20)
                need_update = True
            if mouse_pressed[MIDDLE]:
                pg.draw.circle(sc, GREEN, mouse_position, 20)
                need_update = True
            if mouse_pressed[RIGHT]:
                pg.draw.circle(sc, BLUE, mouse_position, 20)
                need_update = True

            if need_update:
                pg.display.update()


if __name__ == '__main__':
    main()
