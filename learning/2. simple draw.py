import os

from loguru import logger
import pygame

FPS = os.environ.get("FPS", 30)
MOVE_DELTA = 30
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

    @staticmethod
    def set_normal_screen_title():
        pygame.display.set_caption("Движение прямоугольника")

    def move_down(self, delta: int) -> None:
        if self.rect.y + self.rect.height + delta > HEIGHT:
            pygame.display.set_caption("Вниз нельзя")
            return
        self.set_normal_screen_title()
        self.rect.y += delta

    def move_up(self, delta: int) -> None:
        if self.rect.y - delta < 0:
            pygame.display.set_caption("Вверх нельзя")
            return
        self.set_normal_screen_title()
        self.rect.y -= delta

    def move_left(self, delta: int) -> None:
        if self.rect.x - delta < 0:
            pygame.display.set_caption("Влево нельзя")
            return
        self.set_normal_screen_title()
        self.rect.x -= delta

    def move_right(self, delta: int) -> None:
        if self.rect.x + self.rect.width + delta > WIDTH:
            pygame.display.set_caption("Вправо нельзя")
            return
        self.set_normal_screen_title()
        self.rect.x += delta


def main():
    logger.info(f"{FPS = }")
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Тут будут фигурки)")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    player_move_actions = {
        pygame.K_DOWN: player.move_down,
        pygame.K_UP: player.move_up,
        pygame.K_LEFT: player.move_left,
        pygame.K_RIGHT: player.move_right
    }

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            logger.debug(event)
            if event.type == pygame.QUIT:
                logger.debug("Выходим!")
                return
            if event.type == pygame.KEYDOWN and event.key in player_move_actions:
                logger.info(f"Двигаем прямоугольник, {player.rect}")
                player_move_actions[event.key](MOVE_DELTA)
        all_sprites.update()
        surface.fill(BLACK)
        all_sprites.draw(surface)
        pygame.display.flip()


if __name__ == '__main__':
    main()
