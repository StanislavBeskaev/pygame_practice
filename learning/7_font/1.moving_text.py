import pygame as pg

Color = tuple[int, int, int]
Point = tuple[int, int]


class MovingText:
    def __init__(self, text: str, font: pg.font.Font, color: Color, place: Point, antialias: bool = True):
        self._text = font.render(text, antialias, color)
        self._place = self._text.get_rect(center=place)

    @property
    def surface(self) -> pg.Surface:
        return self._text

    @property
    def place(self) -> pg.Rect:
        return self._place

    def update(self) -> None:
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

    def _move_down(self) -> None:
        self._place.y += 1

    def _move_up(self) -> None:
        self._place.y -= 1

    def _move_left(self) -> None:
        self._place.x -= 1

    def _move_right(self) -> None:
        self._place.x += 1


def main():
    """Текст двигающийся с помощью стрелок"""
    pg.font.init()

    sc = pg.display.set_mode((400, 300))
    sc.fill((200, 255, 200))

    font = pg.font.Font(None, 72)
    text = MovingText(text="Hello World", font=font, color=(0, 100, 0), place=(200, 150))
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
        pg.time.delay(20)


if __name__ == '__main__':
    main()
