from .Vector2 import Vector2


class Player():
    def __init__(self, x: float, y: float, size: int,
                 maze_max_x: int, maze_max_y: int, cell_size: int):
        self.max_x = maze_max_x - size
        self.max_y = maze_max_y - size

        self.__x = 0
        self.__y = 0
        self.x = x * cell_size + cell_size / 2 - size / 2
        self.y = y * cell_size + cell_size / 2 - size / 2

        self.size = size

        self.velocity = Vector2(0, 0)

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value) -> None:
        self.__x = min(max(0, value), self.max_x)

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value) -> None:
        self.__y = min(max(0, value), self.max_y)

    @property
    def center_x(self) -> int:
        return self.__x + self.size / 2

    @property
    def center_y(self) -> int:
        return self.__y + self.size / 2

    @property
    def top_left_corner(self) -> Vector2:
        return Vector2(self.x, self.y)

    @property
    def top_right_corner(self) -> Vector2:
        return Vector2(self.x + self.size - 1, self.y)

    @property
    def bottom_left_corner(self) -> Vector2:
        return Vector2(self.x, self.y + self.size - 1)

    @property
    def bottom_right_corner(self) -> Vector2:
        return Vector2(self.x + self.size - 1, self.y + self.size - 1)
