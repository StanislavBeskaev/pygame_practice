import sys

import pygame as pg

WHITE = (255, 255, 255)
BLUE = (0, 0, 225)

pg.init()
sc = pg.display.set_mode((800, 500))
sc.fill(WHITE)
pg.display.update()

pg.mouse.set_visible(False)

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

    sc.fill(WHITE)

    if pg.mouse.get_focused():
        pos = pg.mouse.get_pos()
        pg.draw.rect(sc, BLUE, (pos[0] - 10, pos[1] - 10, 30, 30))

    pg.display.update()
    pg.time.delay(20)
