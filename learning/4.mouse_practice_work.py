from dataclasses import dataclass

from loguru import logger
import pygame as pg


FPS = 60
SPEED = 5
WIDTH = 800
HEIGHT = 500
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
LEFT_MOUSE_BUTTON = 1

Color = tuple[int, int, int]


@dataclass
class Point:
    x: int
    y: int


class Bullet:
    CIRCLE_RADIUS = 20

    def __init__(self, x: int, color: Color, target: Point):
        self._x = x
        self._y = HEIGHT - self.CIRCLE_RADIUS
        self._color = color
        self._target = target

    def move(self, delta: int, surface: pg.Surface) -> bool:
        if self._y > self._target.y:
            self._y -= delta
            self._draw(surface=surface)
            return True

        return False

    def _draw(self, surface: pg.Surface) -> None:
        pg.draw.circle(
            surface=surface,
            color=self._color,
            center=(self._x, self._y),
            radius=self.CIRCLE_RADIUS
        )


class Game:
    EXPLOSION_SIZE = 50
    EXPLOSION_FRAMES = FPS // 3

    def __init__(self):
        self._bullet_move = False
        self._target: Point = None  # noqa
        self._bullet: Bullet = None  # noqa
        self._explosion_color: Color = None  # noqa
        self._show_explosion = False
        self._explosion_frames_remain = self.EXPLOSION_FRAMES

    def shoot(self, target: Point, bullet_color: Color, explosion_color: Color) -> None:
        if not self._bullet_move and not self._show_explosion:
            logger.info(f"Стреляем в точку: {target}")
            self._target = target
            self._bullet = Bullet(x=target.x, color=bullet_color, target=target)
            self._bullet_move = True
            self._explosion_color = explosion_color
        else:
            logger.warning("Пока стрелять нельзя")

    def update(self, surface: pg.Surface) -> None:
        surface.fill(WHITE)
        if self._bullet_move:
            can_bullet_move = self._bullet.move(delta=SPEED, surface=surface)
            if not can_bullet_move:
                self._bullet_move = False
                self._show_explosion = True
                self._explosion_frames_remain = self.EXPLOSION_FRAMES
                self._bullet = None
        elif self._show_explosion and self._explosion_frames_remain > 0:
            self._draw_explosion(surface=surface)
            self._explosion_frames_remain -= 1
            self._show_explosion = self._explosion_frames_remain > 0

        pg.display.update()

    def _draw_explosion(self, surface: pg.Surface):
        pg.draw.rect(
            surface=surface,
            color=self._explosion_color,
            rect=(
                self._target.x - 0.5 * self.EXPLOSION_SIZE,
                self._target.y - 0.5 * self.EXPLOSION_SIZE,
                self.EXPLOSION_SIZE,
                self.EXPLOSION_SIZE
            )
        )


def main():
    sc = pg.display.set_mode((WIDTH, HEIGHT))
    sc.fill(WHITE)
    pg.display.update()
    clock = pg.time.Clock()
    game = Game()

    while True:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
                game.shoot(Point(*event.pos), bullet_color=GREEN, explosion_color=RED)
        game.update(surface=sc)


if __name__ == '__main__':
    main()
