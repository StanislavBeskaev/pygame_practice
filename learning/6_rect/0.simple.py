import pygame as pg


def main():
    sc = pg.display.set_mode((400, 400))

    rect1 = pg.Rect((0, 0, 30, 30))
    rect2 = pg.Rect((30, 30, 30, 30))

    print(f"{rect1.bottomright=}")
    print(f"{rect2.bottomright=}")
    print(f"{rect2.topleft=}")

    rect2.move_ip(10, 10)  # Метод move_ip() смещает прямоугольную область по оси x и y
    print("rect2.move_ip(10, 10)")
    print(f"{rect2.topleft=}")

    rect1.union_ip(rect2)  # присоединяет к тому прямоугольнику, к которому применяется, другой – который передается аргументом
    print("rect1.union_ip(rect2)")
    print(f"{rect1.width=}")
    print(f"{rect1.topright=}")

    while True:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return


if __name__ == '__main__':
    main()
