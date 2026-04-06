from constants import *

class Game():
    def __init__(self):
        self.delta_time = 0
        self.__angle = 0
        self.left_rotate = False
        self.right_rotate = False

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        while (value < 0):
            value += 360

        self.__angle = value % 360

    def rotate(self) -> None:
        direction = 0
        if (self.left_rotate):
            direction -= 1
        if (self.right_rotate):
            direction += 1
        self.angle += direction * ROTATION_SPEED * self.delta_time
