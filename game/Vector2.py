from typing import Self

class Vector2():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __mul__(self, v2: Self) -> Self:
        return Vector2(self.x * v2.x, self.y * v2.y)

    def __sub__(self, v2: Self) -> Self:
        return Vector2(self.x - v2.x, self.y - v2.y)
