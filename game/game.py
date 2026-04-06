class Game():
    def __init__(self):
        self.time = 0
        self.__angle = 0

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        while (value < 0):
            value += 360

        self.__angle = value % 360
