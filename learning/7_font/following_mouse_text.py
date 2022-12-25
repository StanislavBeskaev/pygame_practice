import pygame as pg
from pygame.time import Clock

from projects.common.psysics.point import Point
from projects.common.psysics.speed import Speed
from projects.common.psysics.vector import Vector

Color = tuple[int, int, int]
PGPoint = tuple[int, int]
FPS = 60
WIDTH = 1024
HEIGHT = 768


class FollowingMouseText:
    MAX_SPEED = 350
    STOP_MOUSE_FOLLOW_DISTANCE = 10

    def __init__(self, text: str, font: pg.font.Font, color: Color, place: PGPoint, antialias: bool = True):
        self._text = font.render(text, antialias, color)
        self._place = self._text.get_rect(center=place)
        self._moving_by_arrow = False

    @property
    def surface(self) -> pg.Surface:
        return self._text

    @property
    def place(self) -> pg.Rect:
        return self._place

    @property
    def center(self) -> Point:
        return Point.build_from_tuple(self._place.center)

    @property
    def distance_to_mouse(self) -> float:
        return self.center.calculate_distance_to_point(get_mouse_position())

    def update(self) -> None:
        self._moving_by_arrow = False

        keys_action_map = {
            pg.K_LEFT: self._move_left,
            pg.K_RIGHT: self._move_right,
            pg.K_UP: self._move_up,
            pg.K_DOWN: self._move_down,
        }
        keys_state = pg.key.get_pressed()

        for key, action in keys_action_map.items():
            if keys_state[key]:
                action()
                self._moving_by_arrow = True

        if self._need_follow_mouse():
            self._follow_mouse()

    def _follow_mouse(self) -> None:
        mouse_position = get_mouse_position()
        unit_vector_to_mouse = Vector.build_from_points(self.center, mouse_position).get_unit_vector()

        speed = Speed(
            x_pixels_per_second=self.MAX_SPEED * unit_vector_to_mouse.x,
            y_pixels_per_second=self.MAX_SPEED * unit_vector_to_mouse.y,
            fps=FPS,
        )

        self._place.x += speed.get_x_frame_delta()
        self._place.y += speed.get_y_frame_delta()

    def _need_follow_mouse(self) -> bool:
        return self.distance_to_mouse > self.STOP_MOUSE_FOLLOW_DISTANCE and not self._moving_by_arrow

    def _move_down(self) -> None:
        self._place.y += self._get_frame_key_moving_delta()

    def _move_up(self) -> None:
        self._place.y -= self._get_frame_key_moving_delta()

    def _move_left(self) -> None:
        self._place.x -= self._get_frame_key_moving_delta()

    def _move_right(self) -> None:
        self._place.x += self._get_frame_key_moving_delta()

    def _get_frame_key_moving_delta(self) -> float:
        return 0.5 * self.MAX_SPEED / FPS


def get_mouse_position() -> Point:
    return Point.build_from_tuple(pg.mouse.get_pos())


def main():
    """Текст двигающийся с помощью стрелок"""
    pg.font.init()
    clock = Clock()

    sc = pg.display.set_mode((WIDTH, HEIGHT))
    sc.fill((200, 255, 200))

    font = pg.font.Font(None, 72)
    text = FollowingMouseText(text="Hello World", font=font, color=(0, 100, 0), place=(200, 150))
    sc.blit(text.surface, text.place)

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        text.update()
        sc.fill((200, 255, 200))
        sc.blit(text.surface, text.place)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
