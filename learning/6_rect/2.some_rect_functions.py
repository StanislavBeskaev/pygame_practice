import pygame

from learning import colors

X_SPEED = 3
Y_SPEED = 10
FPS = 60


def main():
    """Рисование двигающегося квадрата слева направо и сверху вниз, как доходит до края, то возвращается"""
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((300, 300))
    sc.fill(color=colors.LIGHT_GREEN)

    surf2 = pygame.Surface((100, 100))
    surf2.fill(color=colors.WHITE)

    rect = surf2.get_rect()  # создается Rect, тут есть куча именованных параметров: topleft, centerx...
    sc.blit(surf2, rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if rect.x + rect.width < sc.get_width():
            rect.x += X_SPEED
        else:
            rect.x = 0
            if rect.y + rect.height < sc.get_width():
                rect.y += Y_SPEED
            else:
                rect.y = 0

        sc.fill(color=colors.LIGHT_GREEN)
        sc.blit(surf2, rect)
        pygame.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
