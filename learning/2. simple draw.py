import os

from loguru import logger
import pygame


FPS = os.environ.get("FPS", 30)
SPEED = 5
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WIDTH = 600
HEIGHT = 400


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self._x_speed = 0
        self._y_speed = 0

    def update(self) -> None:
        self._move_vertically()
        self._move_horizontally()
        self._update_title()

    def _move_vertically(self):
        if not self._can_move_up():
            self.rect.y = 0
        elif not self._can_move_down():
            self.rect.y = HEIGHT - self.rect.height
        else:
            self.rect.y += self._y_speed

    def _move_horizontally(self):
        if not self._can_move_left():
            self.rect.x = 0
        elif not self._can_move_right():
            self.rect.x = WIDTH - self.rect.width
        else:
            self.rect.x += self._x_speed

    def _update_title(self) -> None:
        horizontal_break = None
        vertical_break = None

        if not self._can_move_right():
            horizontal_break = "вправо"
        if not self._can_move_left():
            horizontal_break = "влево"

        if not self._can_move_up():
            vertical_break = "вверх"
        if not self._can_move_down():
            vertical_break = "вниз"

        if not horizontal_break and not vertical_break:
            pygame.display.set_caption("Можно двигаться во все стороны")
        elif horizontal_break and vertical_break:
            pygame.display.set_caption(f"Упёрлись в угол, {horizontal_break} и {vertical_break} нельзя")
        elif horizontal_break:
            pygame.display.set_caption(f"Упёрлись в край, {horizontal_break} нельзя")
        else:
            # только по вертикали нельзя двигаться
            pygame.display.set_caption(f"Упёрлись в край, {vertical_break} нельзя")

    def start_move_down(self) -> None:
        self._y_speed += SPEED

    def stop_move_down(self) -> None:
        self._y_speed -= SPEED

    def start_move_up(self) -> None:
        self._y_speed -= SPEED

    def stop_move_up(self) -> None:
        self._y_speed += SPEED

    def start_move_left(self) -> None:
        self._x_speed -= SPEED

    def stop_move_left(self) -> None:
        self._x_speed += SPEED

    def start_move_right(self) -> None:
        self._x_speed += SPEED

    def stop_move_right(self) -> None:
        self._x_speed -= SPEED

    def _can_move_right(self) -> bool:
        return self.rect.x + self.rect.width + self._x_speed < WIDTH

    def _can_move_left(self) -> bool:
        return self.rect.x + self._x_speed > 0

    def _can_move_up(self) -> bool:
        return self.rect.y + self._y_speed > 0

    def _can_move_down(self) -> bool:
        return self.rect.y + self.rect.height + self._y_speed < HEIGHT


def main():
    logger.info(f"{FPS = }")
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Тут будут фигурки)")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    player_start_move_actions = {
        pygame.K_DOWN: player.start_move_down,
        pygame.K_UP: player.start_move_up,
        pygame.K_LEFT: player.start_move_left,
        pygame.K_RIGHT: player.start_move_right
    }

    player_stop_move_actions = {
        pygame.K_DOWN: player.stop_move_down,
        pygame.K_UP: player.stop_move_up,
        pygame.K_LEFT: player.stop_move_left,
        pygame.K_RIGHT: player.stop_move_right
    }

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            logger.debug(event)
            if event.type == pygame.QUIT:
                logger.debug("Выходим!")
                return
            if event.type == pygame.KEYDOWN and event.key in player_start_move_actions:
                logger.info(f"Инициализация движения прямоугольника, {player.rect}")
                player_start_move_actions[event.key]()
            if event.type == pygame.KEYUP and event.key in player_stop_move_actions:
                logger.info(f"Останавливаем движения прямоугольника, {player.rect}")
                player_stop_move_actions[event.key]()

        all_sprites.update()
        surface.fill(BLACK)
        all_sprites.draw(surface)
        pygame.display.flip()


if __name__ == '__main__':
    main()
