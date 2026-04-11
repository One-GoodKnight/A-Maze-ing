from .cell import Cell
from .directions import Direction
from typing import Optional
from random import randint

class WallBuilder():
    @staticmethod
    def build_wall(maze: list[list[Optional[Cell]]]) -> None:
        for row in maze:
            for cell in row:
                if not cell:
                    continue
                cell.north = not cell.dir_north
                cell.east = not cell.dir_east
                cell.south = not cell.dir_south
                cell.west = not cell.dir_west

    @staticmethod
    def add_solutions(maze: list[list[Optional[Cell]]], logo: list[Cell], max_x: int, max_y: int, n: int) -> None:
        for i in range(n):
            rand_x, rand_y = (randint(0, max_x), randint(0, max_y))
