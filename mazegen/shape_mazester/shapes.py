from .directions import Direction
from collections.abc import Generator
from math import sqrt, acos, pi
from enum import Enum
from typing import Callable


class Shape(Enum):
    """Enum that exposes the available shapes for the maze generation."""
    TRIANGLE = 'triangle'
    SQUARE = 'square'
    CIRCLE = 'circle'

    def get_func(self) -> Callable[[], Generator[float, None, None]]:
        """Returns the appropriate function to get a generator of angles for
        the shape instanciated."""
        return {
            Shape.TRIANGLE: Shapes.triangle,
            Shape.SQUARE: Shapes.square,
            Shape.CIRCLE: Shapes.circle,
        }[self]


class Vertex():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    @staticmethod
    def distance(v1: "Vertex", v2: "Vertex") -> float:
        dx = abs(v2.x - v1.x)
        dy = abs(v2.y - v1.y)

        d = sqrt(dx ** 2 + dy ** 2)
        return d


class Segment():
    def __init__(self, v1: Vertex, v2: Vertex, length: float) -> None:
        self.v1 = v1
        self.v2 = v2
        self.length = length

    def __repr__(self) -> str:
        return f"({self.v1}, {self.v2}, {self.length})"


class Shapes():
    @staticmethod
    def normalize_vector(vector: tuple[float, float]) -> tuple[float, float]:
        magnitude = sqrt(vector[0] ** 2 + vector[1] ** 2)
        return (vector[0] / magnitude, vector[1] / magnitude)

    @staticmethod
    def construct_shape_gen(
        verticies_tuple: list[tuple[float, float]]
    ) -> Generator[float, None, None]:
        coeff: float = 6.
        coeff /= 1000

        verticies: list[Vertex] = []
        for v in verticies_tuple:
            verticies.append(Vertex(x=int(v[0]), y=int(v[1])))

        segments: list[Segment] = []
        for i in range(len(verticies) - 1):
            new_seg = Segment(verticies[i], verticies[i + 1],
                              Vertex.distance(verticies[i], verticies[i + 1]))
            segments.append(new_seg)
        new_seg = Segment(verticies[-1], verticies[0],
                          Vertex.distance(verticies[-1], verticies[0]))
        segments.append(new_seg)

        perimeter = sum([s.length for s in segments])
        step_amount: float = (perimeter) * coeff

        distance = 1

        i_seg = 0
        cur_distance_seg: float = 0.

        while True:
            step_remaining = step_amount / distance

            distance_to_seg_end = segments[i_seg].length - cur_distance_seg
            while distance_to_seg_end < step_remaining:
                step_remaining -= distance_to_seg_end

                if i_seg == len(segments) - 1:
                    distance += 1
                i_seg = (i_seg + 1) % len(segments)
                cur_distance_seg = 0

                distance_to_seg_end = segments[i_seg].length

            cur_distance_seg += step_remaining

            cur_seg = segments[i_seg]

            t = cur_distance_seg / cur_seg.length
            dx = cur_seg.v2.x - cur_seg.v1.x
            dy = cur_seg.v2.y - cur_seg.v1.y

            res_posx = cur_seg.v1.x + dx * t
            res_posy = cur_seg.v1.y + dy * t

            vector = (res_posx, res_posy)
            normed = Shapes.normalize_vector(vector)

            yield (acos(normed[0]) if normed[1] < 0
                   else -acos(normed[0]))

    @staticmethod
    def triangle() -> Generator[float, None, None]:
        triangle = Shapes.construct_shape_gen(
            [(0., 1.), (1., -1.), (-1., -1.)]
        )
        while True:
            yield next(triangle)

    @staticmethod
    def square() -> Generator[float, None, None]:
        direction = Direction.SOUTH
        vector: list[float] = [1., 0.]
        coeff: float = 7 / 1000
        step_amount: float = (2 * (1 + 1)) * coeff
        step: float = 0.

        while True:
            distance = step // (2 * pi)
            if distance < 1:
                distance = 1
            match direction:
                case Direction.SOUTH:
                    vector[1] += step_amount / distance
                case Direction.NORTH:
                    vector[1] -= step_amount / distance
                case Direction.EAST:
                    vector[0] += step_amount / distance
                case Direction.WEST:
                    vector[0] -= step_amount / distance

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

            normed = Shapes.normalize_vector((vector[0], vector[1]))
            step += step_amount / (distance if distance > 1 else 1)
            yield (acos(normed[0]) if normed[1] >= 0
                   else -acos(normed[0]))

    @staticmethod
    def circle() -> Generator[float, None, None]:
        # coeff helps adding chaos to the maze, with a lower coeff,
        # the maze can generate multiple cells using the same raycast
        # that helps breaking the uniformity of the maze

        # with a high value, each cell generation will be independent
        # of the other cells because there wasn't a cell generated right next
        # to it that constrains it's generation that results in a maze
        # full of straight lines towards the starting cell

        coeff: float = 11 / 1000
        step_amount: float = (2 * pi) * coeff
        step: float = 0.
        while (True):
            yield (step % (2 * pi))
            distance = step // (2 * pi)
            step += step_amount / (distance if distance > 1 else 1)
