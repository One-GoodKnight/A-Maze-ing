from maze_generator import Direction

class Player():
    def __init__(self, x: float, y: float, size: int, max_x: int, max_y: int, color: int):
        self.max_x = max_x
        self.max_y = max_y

        self.__x = 0
        self.__y = 0
        self.x = x
        self.y = y

        self.size = size

        self.color = color
        self.direction = Direction.SOUTH

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
