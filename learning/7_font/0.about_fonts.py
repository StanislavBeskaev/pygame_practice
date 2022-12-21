import pygame

from learning import colors


def draw_text():
    pygame.font.init()

    sc = pygame.display.set_mode((300, 200))
    sc.fill(colors.WHITE)

    f1 = pygame.font.Font(None, 36)  # Шрифт по умолчанию
    text1 = f1.render('Hello Привет', True, colors.RED)

    f2 = pygame.font.SysFont('serif', 48)
    text2 = f2.render("World Мир", False, colors.GREEN)

    sc.blit(text1, (10, 50))
    sc.blit(text2, (10, 100))
    pygame.display.update()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == '__main__':
    print(pygame.font.get_fonts())  # Все шрифты в системе
    print(pygame.font.match_font('ArIaL'))  # Расположение шрифта в системе

    draw_text()
