import random

from loguru import logger
import pygame

from projects.common import colors
from projects.common.psysics.point import Point
from projects.common.psysics.speed import Speed

FPS = 30
WIN_WIDTH = 1200
WIN_HEIGHT = 700
MOUSE_LEFT = 1
MOUSE_RIGHT = 3
MAX_BALL_DIRECTION_SPEED = 800
LOG_EVENTS = False


class GameOverException(Exception):
    """Исключение конца игры"""
    pass


class Ball:
    """Игровой шар"""
    def __init__(self, start: Point, color: colors.Color, speed: Speed, radius: int, surface: pygame.Surface):
        self._center = Point.push_back_point_from_surface_borders(point=start, surface=surface, distance=radius)
        self._color = color
        self._speed = speed
        self._radius = radius
        self._collisions_count = 0

    def __repr__(self):
        return f"Ball, точка: {self._center}, скорость: {self._speed}, цвет: {self._color}, радиус: {self._radius}"

    def __str__(self):
        return self.__repr__()

    def draw_on_surface(self, surface: pygame.Surface) -> None:
        """Нарисовать шар на поверхности"""
        pygame.draw.circle(surface, self._color, self._center.to_pygame_point(), self._radius)

    def move(self, surface: pygame.Surface) -> None:
        """Передвинуть шар на поверхности. Меняются координаты шара в зависимости от своей скорости"""
        self._handle_border_collisions(surface=surface)

        # TODO тут забавное изменение скорости
        if self._collisions_count >= 4:
            percent = random.randint(30, 100)
            self._collisions_count = 0
            if self._speed.increase(percent=percent, limit=MAX_BALL_DIRECTION_SPEED):
                logger.info(f"Увеличена скорость на {percent}% для мяча: {self}")

        self._center.x += self._speed.get_x_frame_delta()
        self._center.y += self._speed.get_y_frame_delta()
        self.draw_on_surface(surface=surface)

    def is_point_inside(self, point: Point) -> bool:
        """Попадает ли точки внутрь шара"""
        return self._center.calculate_distance_to_point(point) <= self._radius

    def _handle_border_collisions(self, surface: pygame.Surface) -> None:
        """Обработка столкновений с границами окна"""
        if self._center.is_near_left_border(self._radius):
            self._collisions_count += 1
            self._speed.reflect_by_x()

        if self._center.is_near_top_border(self._radius):
            self._collisions_count += 1
            self._speed.reflect_by_y()

        if self._center.is_near_right_border(distance=self._radius, window_width=surface.get_width()):
            self._collisions_count += 1
            self._speed.reflect_by_x()

        if self._center.is_near_bottom_border(distance=self._radius, window_height=surface.get_height()):
            self._collisions_count += 1
            self._speed.reflect_by_y()


class Game:
    """
    Основной класс игры.
    По ЛКМ создаётся новый шар, по движении мышки с ПКМ удаляются шары.
    Шар изначально летит в случайном направлении.
    После 4 столкновений с границами скорость шара увеличивается. Скорость растёт до предельной скорости
    """

    def __init__(self, fps: int, width: int, height: int, color: colors.Color):
        self._fps = fps
        self._width = width
        self._height = height
        self._clock = pygame.time.Clock()
        self._color = color
        self._surface = pygame.display.set_mode((self._width, self._height))
        self._balls = []
        pygame.display.set_caption("Летающие шары")

    def play(self) -> None:
        """Запуск игры"""
        try:
            while True:
                self._surface.fill(color=self._color)

                for event in pygame.event.get():
                    self._handle_event(event)

                for ball in self._balls:
                    ball.move(surface=self._surface)

                pygame.display.update()
                self._clock.tick(self._fps)
        except GameOverException:
            logger.info("Выходим из игры")
            return

    def _handle_event(self, event: pygame.event.Event) -> None:
        """Обработка входящего события"""
        if LOG_EVENTS:
            logger.debug(f"{event = }")

        if event.type == pygame.QUIT:
            raise GameOverException()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """Обработка нажатия мыши"""
        logger.debug(f"_handle_mouse_click, {event = }")
        click_point = Point.build_from_tuple(event.pos)
        if event.button == MOUSE_LEFT:
            logger.debug("Левая кнопка, добавляем новый шар")
            new_ball = self._create_ball_on_point(click_point)
            self._balls.append(new_ball)
            new_ball.draw_on_surface(self._surface)

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Обработка движения мыши"""
        mouse_point = Point.build_from_tuple(event.pos)

        is_right_press = bool(event.buttons[2])
        if is_right_press:
            self._remove_balls_by_point(mouse_point)

    def _create_ball_on_point(self, point: Point) -> Ball:
        """Создать шар в точке"""
        logger.info(f"Создаём шар в точке: {point}")
        available_colors = (colors.RED, colors.GREEN, colors.YELLOW, colors.BLUE, colors.BLACK, colors.PINK)
        ball_speed = Speed.create_random_speed(max_x=250, max_y=200, fps=self._fps)
        ball = Ball(
            start=point, color=random.choice(available_colors), speed=ball_speed, radius=50, surface=self._surface
        )
        logger.info(f"Создан новый шар: {ball}")
        return ball

    def _remove_balls_by_point(self, point: Point) -> None:
        """Убрать шары в которые попала точка"""
        logger.debug(f"Убираем шары содержащие точку {point = }")
        self._balls = [
            ball
            for ball in self._balls
            if ball not in self._get_ball_containing_point(point)
        ]

    def _get_ball_containing_point(self, point: Point) -> list[Ball]:
        """Получение шаров которые содержат точку"""
        balls = [ball for ball in self._balls if ball.is_point_inside(point)]
        logger.debug(f"Шары содержащие точку {point}: {balls}")
        return balls


def main() -> None:
    game = Game(fps=FPS, width=WIN_WIDTH, height=WIN_HEIGHT, color=colors.WHITE)
    game.play()


if __name__ == '__main__':
    main()
