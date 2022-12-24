import random

import pygame as pg
from pygame.time import Clock

from learning import colors
from projects.common.psysics.point import Point
from projects.common.psysics.vector import Vector

Color = tuple[int, int, int]
PGPoint = tuple[int, int]
FPS = 60
WIDTH = 1024
HEIGHT = 768


class MovableMouseRect:
    """Передвигаемый мышкой прямоугольник"""

    def __init__(self, color: Color, width: int, height: int, x: int, y: int):
        self.surface = pg.Surface((width, height))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._moving = False
        self._previous_mouse_position = None

    def update(self):
        if self._need_start_moving():
            self._start_moving()
        elif self._in_move():
            self._keep_moving()
        elif self._need_stop_moving():
            self._stop_moving()

    def _need_start_moving(self) -> bool:
        # TODO не учитывается ситуация, что мышка была нажата вне прямоугольника и потом очутилась внутри
        return not self._moving and self._is_mouse_inside() and self._is_mouse_left_pressed()

    def _start_moving(self) -> None:
        self._moving = True
        self._previous_mouse_position = Point.build_from_tuple(pg.mouse.get_pos())

    def _in_move(self) -> bool:
        return self._moving and self._is_mouse_left_pressed()

    def _keep_moving(self) -> None:
        new_mouse_position = Point.build_from_tuple(pg.mouse.get_pos())
        mouse_shift = Vector.build_from_points(start=self._previous_mouse_position, end=new_mouse_position)
        self.rect.move_ip(mouse_shift.x, mouse_shift.y)
        self._previous_mouse_position = new_mouse_position

    def _need_stop_moving(self) -> bool:
        return self._moving and not self._is_mouse_left_pressed()

    def _stop_moving(self) -> None:
        self._moving = False
        self._previous_mouse_position = None

    def _is_mouse_inside(self) -> bool:
        """Внутри ли прямоугольника мышь"""
        mouse_position = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_position)

    @staticmethod
    def _is_mouse_left_pressed() -> bool:
        """Нажата ли левая кнопка мыши"""
        return pg.mouse.get_pressed()[0]


def get_mouse_position() -> Point:
    return Point.build_from_tuple(pg.mouse.get_pos())


def main():
    sc = pg.display.set_mode((WIDTH, HEIGHT))
    sc.fill(colors.WHITE)

    rect_width = 200
    rect_height = 150
    rect_count = 15

    available_colors = (
        colors.GREEN, colors.LIGHT_GREEN, colors.BLACK, colors.YELLOW, colors.RED, colors.PINK, colors.BLUE, colors.LIGHT_BLUE
    )

    movable_rects = [
        MovableMouseRect(
            color=random.choice(available_colors),
            width=rect_width,
            height=rect_height,
            x=random.randint(0, WIDTH - rect_width),
            y=random.randint(0, HEIGHT - rect_height)
        )
        for _ in range(rect_count)
    ]
    for movable_rect in movable_rects:
        sc.blit(movable_rect.surface, movable_rect.rect)

    pg.display.update()
    clock = Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        sc.fill(colors.WHITE)

        for movable_rect in movable_rects:
            movable_rect.update()
            sc.blit(movable_rect.surface, movable_rect.rect)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
