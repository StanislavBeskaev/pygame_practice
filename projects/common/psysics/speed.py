import random


class Speed:
    """Скорость передвижения по плоскости"""
    MAX_PIXEL_PER_SECOND = 600

    def __init__(self, x_pixels_per_second: float, y_pixels_per_second: float, fps: int):
        self._x_pixels_per_second = x_pixels_per_second
        self._y_pixels_per_second = y_pixels_per_second
        self._fps = fps

    def __str__(self):
        data = f"x_pixels_per_second = {self._x_pixels_per_second}," \
               f" _y_pixels_per_second={self._y_pixels_per_second}, fps={self._fps}"
        return data

    @classmethod
    def create_random_speed(cls, max_x: int, max_y: int, fps) -> "Speed":
        """Создать случайную скорость в заданных пределах"""
        return Speed(
            x_pixels_per_second=random.randint(-max_x, max_x),
            y_pixels_per_second=random.randint(-max_y, max_y),
            fps=fps
        )

    def increase(self, percent: int, limit: int = MAX_PIXEL_PER_SECOND) -> bool:
        if self._can_increase(limit=limit):
            coefficient = (100 + percent) / 100
            self._x_pixels_per_second *= coefficient
            self._y_pixels_per_second *= coefficient
            return True

        return False

    def get_x_frame_delta(self) -> float:
        """Получение смещения по оси x за кадр"""
        return self._get_frame_delta(speed_component=self._x_pixels_per_second)

    def get_y_frame_delta(self) -> float:
        """Получение смещения по оси y за кадр"""
        return self._get_frame_delta(speed_component=self._y_pixels_per_second)

    def reflect_by_x(self) -> None:
        """Отразить скорость по оси x"""
        self._x_pixels_per_second = - self._x_pixels_per_second

    def reflect_by_y(self) -> None:
        """Отразить скорость по оси y"""
        self._y_pixels_per_second = - self._y_pixels_per_second

    def _get_frame_delta(self, speed_component: float) -> float:
        return speed_component / self._fps

    def _can_increase(self, limit: int = MAX_PIXEL_PER_SECOND) -> bool:
        """Можно ли увеличить скорость: не достигнут ли предел по скорости"""
        return (
                - limit < self._x_pixels_per_second < limit
                and - limit < self._y_pixels_per_second < limit
        )
