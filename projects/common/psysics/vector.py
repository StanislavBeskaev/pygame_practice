import math
from dataclasses import dataclass

from projects.common.psysics.point import Point


@dataclass
class Vector:
    """Вектор на плоскости"""
    x: float
    y: float

    @classmethod
    def build_from_points(cls, start: Point, end: Point) -> "Vector":
        """Построение вектора из начальной точки в конечную"""
        return Vector(x=end.x - start.x, y=end.y - start.y)

    @property
    def length(self) -> float:
        """Длина вектора"""
        return math.sqrt(self.x**2 + self.y**2)

    def get_unit_vector(self) -> "Vector":
        """Получение вектора с тем же направлением и длины 1"""
        length = self.length
        return Vector(x=self.x / length, y=self.y / length)
