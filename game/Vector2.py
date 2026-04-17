class Vector2():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __mul__(self, v2: "Vector2") -> "Vector2":
        return Vector2(self.x * v2.x, self.y * v2.y)

    def __sub__(self, v2: "Vector2") -> "Vector2":
        return Vector2(self.x - v2.x, self.y - v2.y)

    def __repr__(self) -> str:
        s = 'Vec2 {\n'
        s += f'\t\tx = {self.x}\n'
        s += f'\t\ty = {self.y}\n'
        s += '\t}'
        return s
