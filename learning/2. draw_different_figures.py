import math
import os

import pygame
from loguru import logger

FPS = os.environ.get("FPS", 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

SPEED = 5
WIDTH = 800
HEIGHT = 600


def main():
    logger.info(f"{FPS = }")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Тут будут фигурки)")
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            logger.debug(event)
            if event.type == pygame.QUIT:
                logger.debug("Выходим!")
                return
        pygame.display.update()
        pygame.draw.rect(surface, WHITE, (20, 20, 100, 75))  # координаты верхнего левого угла, ширина и высота
        pygame.draw.rect(surface, LIGHT_BLUE, (150, 20, 100, 75), 8)

        pygame.draw.line(surface, WHITE, [10, 250], [290, 200], 3)  # линия из какой точки в какую, ширина
        pygame.draw.line(surface, GREEN, [10, 260], [290, 210], 10)
        pygame.draw.aaline(surface, WHITE, [10, 270], [290, 220])

        pygame.draw.aalines(surface, YELLOW, False, ((10, 280), (290, 230), (290, 270), (150, 290)))

        pygame.draw.polygon(surface, WHITE, [[350, 10], [380, 50], [290, 90], [230, 30]])
        pygame.draw.polygon(surface, WHITE, [[450, 110], [480, 150], [390, 190], [330, 130]])
        pygame.draw.aalines(surface, WHITE, True, [[450, 110], [480, 150], [390, 190], [330, 130]])

        pygame.draw.circle(surface, YELLOW, (400, 300), 50)
        pygame.draw.circle(surface, PINK, (500, 300), 50, 45, draw_top_right=True)
        pygame.draw.ellipse(surface, GREEN, (10, 350, 280, 100))

        pygame.draw.arc(surface, WHITE, (510, 50, 280, 100), 0, math.pi)
        pygame.draw.arc(surface, PINK, (550, 30, 200, 150), math.pi, 2 * math.pi, 3)


if __name__ == '__main__':
    main()
