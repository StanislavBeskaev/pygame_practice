import random

import pygame as pg
from pygame.time import Clock

from learning import colors
from projects.common.psysics.point import Point
from projects.common.psysics.vector import Vector

Color = tuple[int, int, int]
PGPoint = tuple[int, int]
FPS = 35
WIDTH = 1024
HEIGHT = 768

last_mouse_pressed_position: PGPoint
movable_rects: list["MovableMouseRect"] = []
RECT_COUNT = 60
RECT_MIN_WIDTH = 60
RECT_MAX_WIDTH = 200
RECT_MIN_HEIGHT = 40
RECT_MAX_HEIGHT = 150
PASSIVE_BORDER_COLOR = colors.GRAY
ACTIVE_BORDER_COLOR = colors.ORANGE
PASSIVE_BORDER_WIDTH = 1
ACTIVE_BORDER_WIDTH = 3


class MovableMouseRect:
    """Передвигаемый мышкой прямоугольник"""

    def __init__(self, color: Color, width: int, height: int, x: int, y: int, text_size: int = 25):
        self._width = width
        self._height = height
        self._color = color
        self.surface = pg.Surface((width, height))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = False
        self._previous_mouse_position = None

        self._intersection_count = 0
        self._font = pg.font.Font(None, text_size)

    def update(self):
        if self._need_start_moving():
            self._start_moving()
        elif self._in_move():
            self._keep_moving()
        elif self._need_stop_moving():
            self._stop_moving()

        self._calculate_intersection_count()
        self.surface.fill(ACTIVE_BORDER_COLOR if self.moving else PASSIVE_BORDER_COLOR)
        border_width = ACTIVE_BORDER_WIDTH if self.moving else PASSIVE_BORDER_WIDTH
        self.surface.fill(self._color, self.surface.get_rect().inflate(-2 * border_width, -2 * border_width))
        self._display_intersection_count()

    def _need_start_moving(self) -> bool:
        return (
            not self.moving
            and _is_mouse_left_pressed()
            and self._is_mouse_pressed_inside()
            and not is_any_movable_rect_moving()
        )

    def _start_moving(self) -> None:
        self.moving = True
        self._previous_mouse_position = Point.build_from_tuple(pg.mouse.get_pos())

    def _in_move(self) -> bool:
        return self.moving and _is_mouse_left_pressed()

    def _keep_moving(self) -> None:
        new_mouse_position = Point.build_from_tuple(pg.mouse.get_pos())
        mouse_shift = Vector.build_from_points(start=self._previous_mouse_position, end=new_mouse_position)
        self.rect.move_ip(mouse_shift.x, mouse_shift.y)
        self._previous_mouse_position = new_mouse_position

    def _need_stop_moving(self) -> bool:
        return self.moving and not _is_mouse_left_pressed()

    def _stop_moving(self) -> None:
        self.moving = False
        self._previous_mouse_position = None

    def _is_mouse_pressed_inside(self) -> bool:
        """Была ли нажата левая кнопка мыши внутри прямоугольника"""
        global last_mouse_pressed_position
        return self.rect.collidepoint(last_mouse_pressed_position)

    def _calculate_intersection_count(self) -> None:
        intersected_rects = [
            movable_rect
            for movable_rect in movable_rects
            if movable_rect is not self and self.rect.colliderect(movable_rect.rect)
        ]

        self._intersection_count = len(intersected_rects)

    def _display_intersection_count(self) -> None:
        number = str(self._intersection_count)
        text = self._font.render(number, True, colors.BLACK)
        self.surface.blit(text, (self._width - 7 - 7 * len(number), 7))


def get_mouse_position() -> Point:
    return Point.build_from_tuple(pg.mouse.get_pos())


def fill_movable_rects() -> None:
    global movable_rects

    movable_rects = []

    available_colors = (
        colors.GREEN,
        colors.LIGHT_GREEN,
        colors.YELLOW,
        colors.RED,
        colors.PINK,
        colors.BLUE,
        colors.LIGHT_BLUE,
    )

    for _ in range(RECT_COUNT):
        rect_width = random.randint(RECT_MIN_WIDTH, RECT_MAX_WIDTH)
        rect_height = random.randint(RECT_MIN_HEIGHT, RECT_MAX_HEIGHT)

        movable_rects.append(
            MovableMouseRect(
                color=random.choice(available_colors),
                width=rect_width,
                height=rect_height,
                x=random.randint(0, WIDTH - rect_width),
                y=random.randint(0, HEIGHT - rect_height),
            )
        )


def is_any_movable_rect_moving() -> bool:
    global movable_rects
    return any([rect.moving for rect in movable_rects])


def main():
    global movable_rects
    global last_mouse_pressed_position

    pg.font.init()
    sc = pg.display.set_mode((WIDTH, HEIGHT))
    sc.fill(colors.WHITE)

    fill_movable_rects()

    pg.display.update()
    clock = Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                last_mouse_pressed_position = pg.mouse.get_pos()

            if event.type == pg.KEYUP and event.key == pg.K_r and not _is_mouse_left_pressed():
                fill_movable_rects()

        sc.fill(colors.WHITE)

        # В обратном порядке, что бы сначала двигались прямоугольники на переднем фоне
        for movable_rect in movable_rects[::-1]:
            movable_rect.update()

        movable_rects = sorted(movable_rects, key=lambda rect: rect.moving)

        for movable_rect in movable_rects:
            sc.blit(movable_rect.surface, movable_rect.rect)

        pg.display.update()
        clock.tick(FPS)


def _is_mouse_left_pressed() -> bool:
    """Нажата ли левая кнопка мыши"""
    return pg.mouse.get_pressed()[0]


if __name__ == '__main__':
    main()
