from .cell import Cell
from .directions import Direction
from typing import Optional

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
