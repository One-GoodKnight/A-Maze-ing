from typing import Tuple
import math


class RayCast():
    @staticmethod
    def cast_ray(start: Tuple[int, int], angle: float,
                 max_x: int, max_y: int) -> list[Tuple[int, int]]:
        cells: list[Tuple[int, int]] = []

        dir_x = math.cos(angle)
        dir_y = math.sin(angle)

        x = start[0]
        y = start[1]

        step_dir_x = 1 if dir_x >= 0 else -1
        step_dir_y = 1 if dir_y >= 0 else -1

        t_delta_x = abs(1 / dir_x) if dir_x != 0 else math.inf
        t_delta_y = abs(1 / dir_y) if dir_y != 0 else math.inf

        t_next_x = (0.5 / abs(dir_x)) if dir_x != 0 else math.inf
        t_next_y = (0.5 / abs(dir_y)) if dir_y != 0 else math.inf

        while (True):
            if (x < 0 or x > max_x or y < 0 or y > max_y):
                return cells
            cells.append((x, y))
            if (t_next_x < t_next_y):
                t_next_x += t_delta_x
                x += step_dir_x
            else:
                t_next_y += t_delta_y
                y += step_dir_y
