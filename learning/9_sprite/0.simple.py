import os
import sys
from random import randint

import pygame as pg
from loguru import logger

WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
IMAGES_FOLDER = "images"


class Car(pg.sprite.Sprite):
    def __init__(self, x, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 0))

    def is_point_inside(self, x, y) -> bool:
        return self.rect.collidepoint(x, y)


def main():
    sc = pg.display.set_mode((WIDTH, HEIGHT))

    car = Car(x=randint(1, WIDTH), filename=os.path.join(IMAGES_FOLDER, "car1.png"))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                logger.debug("Нажата мышь!")
                coordinates = event.pos
                if car.is_point_inside(*coordinates):
                    logger.error("Попали по машине")
                else:
                    logger.warning("Промазал!")

        sc.fill(WHITE)
        sc.blit(car.image, car.rect)
        pg.display.update()
        pg.time.delay(50)

        # машинка ездит сверху вниз
        if car.rect.y < HEIGHT:
            car.rect.y += 0.02
        else:
            car.rect.y = 0


if __name__ == '__main__':
    main()
