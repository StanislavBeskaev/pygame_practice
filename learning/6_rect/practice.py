from abc import ABC
import random

import pygame

from learning import colors

WIN_WIDTH = 800
WIN_HEIGHT = 600
WIN_CENTER = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
CIRCLE_RADIUS = 250
FPS = 5
AVAILABLE_COLORS = (
        colors.BLACK,
        colors.PINK,
        colors.RED,
        colors.YELLOW,
        colors.GREEN,
        colors.LIGHT_GREEN,
        colors.LIGHT_BLUE,
        colors.GRAY
    )


class CircleQuarter(ABC):
    """Четверть круга"""
    common_change_color_key = pygame.K_0
    quarter_change_color_key = None
    draw_attrs = {}

    def __init__(self, center: tuple[int, int], radius: int):
        self._center = center
        self._radius = radius
        self._color = random.choice(AVAILABLE_COLORS)

    def update(self, surface: pygame.Surface) -> None:
        if self._is_need_change_color():
            self._change_color()

        self._draw(surface=surface)

    def _is_need_change_color(self) -> bool:
        keys_state = pygame.key.get_pressed()

        return keys_state[self.common_change_color_key] or keys_state[self.quarter_change_color_key]

    def _change_color(self) -> None:
        next_color = self._color
        while next_color == self._color:
            next_color = random.choice(AVAILABLE_COLORS)

        self._color = next_color

    def _draw(self, surface: pygame.Surface) -> None:
        """Нарисовать на поверхности"""
        pygame.draw.circle(
            surface=surface, color=self._color, center=self._center, radius=self._radius, **self.draw_attrs
        )


class TopLeftCircleQuarter(CircleQuarter):
    """Верхняя левая четверть круга"""

    quarter_change_color_key = pygame.K_1
    draw_attrs = {"draw_top_left": True}


class TopRightCircleQuarter(CircleQuarter):
    """Верхняя правая четверть круга"""

    quarter_change_color_key = pygame.K_2
    draw_attrs = {"draw_top_right": True}


class BottomRightCircleQuarter(CircleQuarter):
    """Нижняя правая четверть круга"""

    quarter_change_color_key = pygame.K_3
    draw_attrs = {"draw_bottom_right": True}


class BottomLeftCircleQuarter(CircleQuarter):
    """Нижняя левая четверть круга"""

    quarter_change_color_key = pygame.K_4
    draw_attrs = {"draw_bottom_left": True}


def main():
    """
    Рисование круга поделённого на 4 четверти меняющие цвет по нажатию на клавиши 1-4.
    При нажатии на 0 меняется цвет всего круга
    """
    surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    surface.fill(color=colors.WHITE)

    quarters = _construct_quarters()

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            for quarter in quarters:
                quarter.update(surface=surface)

            pygame.display.update()


def _construct_quarters() -> list[CircleQuarter]:
    quarter_params = {"center": WIN_CENTER, "radius": CIRCLE_RADIUS}
    quarter_classes = (TopLeftCircleQuarter, TopRightCircleQuarter, BottomRightCircleQuarter, BottomLeftCircleQuarter)

    quarters = [quarter_class(**quarter_params) for quarter_class in quarter_classes]

    return quarters


if __name__ == '__main__':
    main()
