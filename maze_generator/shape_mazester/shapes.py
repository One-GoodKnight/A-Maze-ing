from ..directions import Direction
from collections.abc import Generator
import math
from enum import Enum


class Shape(Enum):
    TRIANGLE = 'triangle'
    SQUARE = 'square'
    CIRCLE = 'circle'

    def get_func(self):
        return {
            Shape.TRIANGLE: Shapes.triangle,
            Shape.SQUARE: Shapes.square,
            Shape.CIRCLE: Shapes.circle,
        }[self]


class Shapes():
    @staticmethod
    def normalize_vector(vector: list[float, float]) -> list[float, float]:
        magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        return [vector[0] / magnitude, vector[1] / magnitude]

    @staticmethod
    def triangle(max_x: int, max_y: int):
        pass

    @staticmethod
    def square(max_x: int, max_y: int) -> Generator[float, None, None]:
        direction = Direction.SOUTH
        vector = [1, 0]
        perimeter = (2 * (max_x + max_y + 2))
        coeff = 2
        step_amount = (2 * math.pi) / perimeter * coeff
        step = 0
        
        while True:
            distance = step // (2 * math.pi)
            match direction:
                case Direction.SOUTH:
                    vector[1] += step_amount / (distance if distance > 1 else 1)
                case Direction.NORTH:
                    vector[1] -= step_amount / (distance if distance > 1 else 1)
                case Direction.EAST:
                    vector[0] += step_amount / (distance if distance > 1 else 1)
                case Direction.WEST:
                    vector[0] -= step_amount / (distance if distance > 1 else 1)

            if vector[0] > 1:
                vector[0] = 1
                direction = Direction.SOUTH
            elif vector[0] < -1:
                vector[0] = -1
                direction = Direction.NORTH
            elif vector[1] < -1:
                vector[1] = -1
                direction = Direction.EAST
            elif vector[1] > 1:
                vector[1] = 1
                direction = Direction.WEST

            normed = Shapes.normalize_vector(vector)
            step += step_amount / (distance if distance > 1 else 1)
            yield math.acos(normed[0]) if normed[1] >= 0 else -math.acos(normed[0])

    @staticmethod
    def circle(max_x: int, max_y: int) -> Generator[float, None, None]:
        radius = max(max_x, max_y)
        perimeter = (2 * math.pi * radius)
        step_amount = (2 * math.pi) / perimeter
        # coeff helps adding chaos to the maze, with a lower coeff, the maze can generate multiple cells using the same raycast
        # that helps breaking the uniformity of the maze
        # with a high value, each cell generation will be independent of the other cells because there was not a cell generated right next
        # to it that constrains it's generation that results in a maze full of straight lines towards the starting cell
        coeff = 1.2
        step_amount *= coeff
        step = 0
        while (True):
            yield (step % (2 * math.pi))
            distance = step // (2 * math.pi)
            step += step_amount / (distance if distance > 1 else 1)
