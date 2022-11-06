from dataclasses import dataclass
import math


@dataclass
class Point:
    """Точка на плоскости"""

    x: int
    y: int

    @classmethod
    def build_from_tuple(cls, coordinates: tuple[int, int]) -> "Point":
        """Построение точки из кортежа координат"""
        return cls(*coordinates)

    def calculate_distance_to_point(self, other: "Point") -> float:
        """Посчитать расстояние до точки"""
        x_delta = self.x - other.x
        y_delta = self.y - other.y
        distance = math.sqrt(x_delta ** 2 + y_delta ** 2)
        return distance

    def to_pygame_point(self) -> tuple[int, int]:
        return self.x, self.y

    def is_near_top_border(self, distance: int) -> bool:
        """Находится ли точка около верхней границы"""
        return self.y <= distance

    def is_near_left_border(self, distance: int) -> bool:
        """Находится ли точка около левой границы"""
        return self.x <= distance

    def is_near_bottom_border(self, distance: int, window_height: int) -> bool:
        """Находится ли точка около нижней границы"""
        return window_height - distance <= self.y

    def is_near_right_border(self, distance, window_width) -> bool:
        """Находится ли точка около правой границы"""
        return window_width - distance <= self.x
