import pygame as pg

from learning import colors


def main():
    sc = pg.display.set_mode((300, 300))
    sc.fill(colors.LIGHT_GREEN)

    surf1 = pg.Surface((200, 200))
    surf1.fill(colors.YELLOW)

    surf2 = pg.Surface((100, 100))
    surf2.fill(colors.WHITE)
    rect = pg.Rect((70, 20, 0, 0))
    surf1.blit(surf2, rect)

    sc.blit(surf1, rect)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return


if __name__ == '__main__':
    main()
