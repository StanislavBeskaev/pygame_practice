from dataclasses import dataclass

import pygame

from learning import colors

FPS = 30
WIN_WIDTH = 1200
WIN_HEIGHT = 700
Color = tuple[int, int, int]


class Speed:
    def __init__(self, pixels_per_second: int):
        self._pixels_per_second = pixels_per_second

    def get_frame_delta(self) -> float:
        return self._pixels_per_second / FPS


class Rocket:
    width_rocket = 20
    height_rocket = 50

    def __init__(self, surface: pygame.Surface, color: Color, speed: Speed):
        self._surface = surface
        self._color = color
        self.x = surface.get_width() // 2 - self.width_rocket // 2
        self.y = surface.get_height()
        self._speed = speed

    def fly(self):
        """Вызов метода fly() поднимает ракету на скорость ракеты.
        Если ракета скрывается вверху, она снова появится снизу"""
        pygame.draw.rect(self._surface, self._color, (self.x, self.y, Rocket.width_rocket, Rocket.height_rocket))
        self.y -= self._speed.get_frame_delta()
        if self.y < -Rocket.height_rocket:
            self.y = WIN_HEIGHT


class RocketArea:
    def __init__(self, start_x: int, width: int, color: Color, rocket_color: Color, rocket_speed: Speed):
        self._start_x = start_x
        self._width = width
        self._color = color
        self._active = False
        self._surface = pygame.Surface((width, WIN_HEIGHT))
        self._surface.fill(color)
        self._rocket = Rocket(surface=self._surface, color=rocket_color, speed=rocket_speed)
        self._rocket_speed = rocket_speed

    @property
    def upper_left_corner(self) -> tuple[int, int]:
        return self._start_x, 0

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @property
    def active(self) -> bool:
        return self._active

    def try_click(self, x: int):
        if self._start_x < x < self._start_x + self._width:
            self._active = not self._active

    def update(self, parent_surface: pygame.Surface):
        if not self._active:
            return
        self._surface.fill(self._color)
        self._rocket.fly()
        parent_surface.blit(self._surface, self.upper_left_corner)


@dataclass
class InputRocketArea:
    color: Color
    rocket_color: Color
    rocket_speed: Speed


def build_rocket_areas(input_rocket_areas: list[InputRocketArea]) -> list[RocketArea]:
    rocket_areas_amount = len(input_rocket_areas)
    rocket_area_width = WIN_WIDTH // rocket_areas_amount
    built_rocket_areas = []
    for index, input_rocket_area in enumerate(input_rocket_areas):
        built_rocket_areas.append(
            RocketArea(
                start_x=index * rocket_area_width,
                width=rocket_area_width,
                color=input_rocket_area.color,
                rocket_color=input_rocket_area.rocket_color,
                rocket_speed=input_rocket_area.rocket_speed,
            )
        )

    return built_rocket_areas


def main():
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    rocket_areas = build_rocket_areas(
        input_rocket_areas=[
            InputRocketArea(
                color=colors.WHITE,
                rocket_color=colors.RED,
                rocket_speed=Speed(pixels_per_second=100),
            ),
            InputRocketArea(
                color=colors.LIGHT_BLUE,
                rocket_color=colors.GREEN,
                rocket_speed=Speed(pixels_per_second=150),
            ),
            InputRocketArea(
                color=colors.WHITE,
                rocket_color=colors.BLUE,
                rocket_speed=Speed(pixels_per_second=120),
            )
        ]
    )

    for rocket_area in rocket_areas:
        sc.blit(rocket_area.surface, rocket_area.upper_left_corner)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                event_x = event.pos[0]
                for rocket_area in rocket_areas:
                    rocket_area.try_click(event_x)

        for rocket_area in rocket_areas:
            rocket_area.update(parent_surface=sc)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
