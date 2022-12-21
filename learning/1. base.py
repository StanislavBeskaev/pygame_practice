import os
from datetime import datetime

import pygame
import pytz
from loguru import logger

FPS = os.environ.get("FPS", 30)


def get_screen_title() -> str:
    now = datetime.now(tz=pytz.timezone('Europe/Moscow'))
    formatted_now = now.strftime("%-H:%M:%S %d.%m.%Y")
    screen_title = f"Сейчас {formatted_now}"
    return screen_title


def update_screen_title() -> None:
    pygame.display.set_caption(get_screen_title())


def main():
    logger.debug(f"{FPS = }")
    pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    clock = pygame.time.Clock()  # таймер для управления частотой обновления

    while True:
        clock.tick(FPS)  # таймер сам подберёт нужную задержку под указанную частоту обновления
        update_screen_title()
        for event in pygame.event.get():
            logger.debug(event)
            if event.type == pygame.QUIT:
                logger.debug("Выход, уже?")
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT):
                logger.debug("Нажали мышь")


if __name__ == '__main__':
    main()
