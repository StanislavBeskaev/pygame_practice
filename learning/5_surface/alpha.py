import pygame as pg

from learning import colors

WIDTH = 300
HEIGHT = 200


def main():
    sc = pg.display.set_mode((WIDTH, HEIGHT))
    surf = pg.Surface((200, 150))
    surf.fill(colors.WHITE)
    surf.set_alpha(200)

    # сначала на главной поверхности рисуется зелёный прямоугольник
    pg.draw.rect(sc, colors.GREEN, (0, 80, 300, 40))

    pg.draw.circle(surf, colors.RED, center=(30, 30), radius=30)

    # поверх накладываем полупрозрачную белую поверхность
    sc.blit(surf, (50, 25))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        pg.time.delay(100)


if __name__ == '__main__':
    main()
