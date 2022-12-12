import pygame

from learning import colors

WIN_WIDTH = 800
WIN_HEIGHT = 600
RECT_SIZE = (WIN_WIDTH // 2, WIN_HEIGHT)
FPS = 60


class Rocket:
    width_rocket = 20
    height_rocket = 50

    def __init__(self, surface, color):
        self.surf = surface
        self.color = color
        self.x = surface.get_width() // 2 - Rocket.width_rocket // 2
        self.y = surface.get_height()

    def fly(self):
        pygame.draw.rect(
            self.surf, self.color, (
                self.x, self.y,
                Rocket.width_rocket,
                Rocket.height_rocket))
        self.y -= 3
        if self.y < -Rocket.height_rocket:
            self.y = WIN_HEIGHT


def main():
    sc = pygame.display.set_mode(
        (WIN_WIDTH, WIN_HEIGHT))

    rect_left = pygame.Rect((0, 0), RECT_SIZE)
    rect_right = pygame.Rect((WIN_WIDTH // 2, 0), RECT_SIZE)

    surf_left = pygame.Surface(rect_left.size)
    surf_left.fill(color=colors.WHITE)

    surf_right = pygame.Surface(rect_right.size)

    sc.blit(surf_left, rect_left)
    sc.blit(surf_right, rect_right)

    rocket_left = Rocket(surf_left, color=colors.BLACK)
    rocket_right = Rocket(surf_right, color=colors.WHITE)

    pygame.display.update()

    active_left = True
    active_right = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if rect_left.collidepoint(event.pos):
                    active_left = True
                    active_right = False
                elif rect_right.collidepoint(event.pos):
                    active_right = True
                    active_left = False

        if active_left:
            surf_left.fill(colors.WHITE)
            rocket_left.fly()
            sc.blit(surf_left, rect_left)
            pygame.display.update(rect_left)
        elif active_right:
            surf_right.fill(colors.BLACK)
            rocket_right.fly()
            sc.blit(surf_right, rect_right)
            pygame.display.update(rect_right)

        pygame.time.delay(20)


if __name__ == '__main__':
    main()
