# Напишите код анимационного движения экземпляра Surface, на котором размещены несколько геометрических примитивов,
# нарисованных функциями модуля draw(). Этим примером иллюстрируется группировка графических объектов.
import random
from enum import Enum

import pygame as pg

from learning import colors

WIDTH = 1200
HEIGHT = 700

INNER_SURFACE_WIDTH = 500
INNER_SURFACE_HEIGHT = 300
FPS = 30
MOUSE_LEFT = 1
MOUSE_RIGHT = 3


class Figure(str, Enum):
    RECT = "RECT"
    CIRCLE = "CIRCLE"


class InnerSurface:
    def __init__(self, width: int = INNER_SURFACE_WIDTH, height: int = INNER_SURFACE_HEIGHT):
        self._surface = pg.Surface((width, height))
        self._width = width
        self._height = height
        self.fill()

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def place_figures(self, figures_cnt: int = 5) -> None:
        """Разместить случайные фигуры в количестве figures_cnt"""
        self.fill()
        available_colors = (colors.RED, colors.GREEN, colors.BLUE, colors.YELLOW, colors.PINK)

        for _ in range(figures_cnt):
            chosen_figure = random.choice([figure for figure in Figure])
            color = random.choice(available_colors)

            if chosen_figure == Figure.RECT:
                x = random.randint(0, self._width // 2)
                y = random.randint(0, self._height // 2)
                width = random.randint(20, (self._width - x) // 2)
                height = random.randint(20, (self._height - y) // 2)
                pg.draw.rect(surface=self._surface, color=color, rect=(x, y, width, height))
            elif chosen_figure == Figure.CIRCLE:
                x = random.randint(20, self._width // 2)
                y = random.randint(20, self._height // 2)
                radius = min((self._width - x) // 2, ((self._height - y) // 4))
                pg.draw.circle(surface=self._surface, color=color, center=(x, y), radius=radius)

    def fill(self, color: tuple[int, int, int] = colors.WHITE) -> None:
        self._surface.fill(color=color)


def main():
    clock = pg.time.Clock()
    display = pg.display.set_mode((WIDTH, HEIGHT))
    display.fill(colors.BLACK)
    inner_surface = InnerSurface()
    inner_x = 10
    inner_y = 10

    display.blit(inner_surface.surface, (inner_x, inner_y))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    inner_surface.place_figures(3)
                elif event.button == MOUSE_RIGHT:
                    inner_x = random.randint(0, WIDTH - inner_surface.width)
                    inner_y = random.randint(0, HEIGHT - inner_surface.height)
                    display.fill(colors.BLACK)
                display.blit(inner_surface.surface, (inner_x, inner_y))

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
