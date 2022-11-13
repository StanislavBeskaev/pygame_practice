from random import randint

import pygame as pg


# движение красной поверхности по зелёной поверхности,
# которая по клику случайно выстраивается по основной чёрной поверхности
def main():
    sc = pg.display.set_mode((400, 400))

    background = pg.Surface((400, 200))
    background.fill((0, 255, 0))
    xb = 0
    yb = 100

    hero = pg.Surface((100, 100))
    hero.fill((255, 0, 0))
    x = 0
    y = 50

    # порядок прорисовки важен!
    background.blit(hero, (x, y))
    sc.blit(background, (xb, yb))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONUP:
                yb = randint(0, 200)

        if x < 400:
            x += 2
        else:
            x = 0

        sc.fill((0, 0, 0))
        background.fill((0, 255, 0))

        background.blit(hero, (x, y))
        sc.blit(background, (xb, yb))

        pg.display.update()

        pg.time.delay(30)


if __name__ == "__main__":
    main()
