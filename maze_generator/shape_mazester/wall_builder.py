from ..cell import Cell
from .directions import Direction
from typing import Optional
from random import randint, choice


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
    def open_all_walls(maze: list[list[Optional[Cell]]], logo: list[Cell],
                       max_x: int, max_y: int, cell: Cell) -> None:
        logo_set = {(c.x, c.y) for c in logo}

        if (cell.x, cell.y) in logo_set:
            return

        if cell.x != 0:
            n = maze[cell.y][cell.x - 1]
            if n not in logo_set:
                cell.west = False
                n.east = False

        if cell.x != max_x:
            n = maze[cell.y][cell.x + 1]
            if n not in logo_set:
                cell.east = False
                n.west = False

        if cell.y != 0:
            n = maze[cell.y - 1][cell.x]
            if n not in logo_set:
                cell.north = False
                n.south = False

        if cell.y != max_y:
            n = maze[cell.y + 1][cell.x]
            if n not in logo_set:
                cell.south = False
                n.north = False

    @staticmethod
    def destructible_walls(maze: list[list[Optional[Cell]]], logo: list[Cell],
                           max_x: int, max_y: int, cell: Cell
                           ) -> list[Direction]:
        destructible_walls = []

        if cell.north and cell.y != 0:
            destructible_walls.append(Direction.NORTH)
        if cell.east and cell.x != max_x:
            destructible_walls.append(Direction.EAST)
        if cell.south and cell.y != max_y:
            destructible_walls.append(Direction.SOUTH)
        if cell.west and cell.x != 0:
            destructible_walls.append(Direction.WEST)

        return destructible_walls

    @staticmethod
    def open_single_wall(maze: list[list[Optional[Cell]]], logo: list[Cell],
                         max_x: int, max_y: int, cell: Cell) -> None:
        logo_set = {(c.x, c.y) for c in logo}

        if (cell.x, cell.y) in logo_set:
            return

        destructible_walls = WallBuilder.destructible_walls(maze, logo,
                                                            max_x, max_y, cell)
        if len(destructible_walls) < 2:
            return

        random_wall = choice(destructible_walls)

        match random_wall:
            case Direction.NORTH:
                n = maze[cell.y - 1][cell.x]
                if (n.x, n.y) in logo_set:
                    return
                if len(WallBuilder.destructible_walls(maze, logo,
                                                      max_x, max_y, n)) < 2:
                    return
                cell.north = False
                n.south = False
            case Direction.EAST:
                n = maze[cell.y][cell.x + 1]
                if (n.x, n.y) in logo_set:
                    return
                if len(WallBuilder.destructible_walls(maze, logo,
                                                      max_x, max_y, n)) < 2:
                    return
                cell.east = False
                n.west = False
            case Direction.SOUTH:
                n = maze[cell.y + 1][cell.x]
                if (n.x, n.y) in logo_set:
                    return
                if len(WallBuilder.destructible_walls(maze, logo,
                                                      max_x, max_y, n)) < 2:
                    return
                cell.south = False
                n.north = False
            case Direction.WEST:
                n = maze[cell.y][cell.x - 1]
                if (n.x, n.y) in logo_set:
                    return
                if len(WallBuilder.destructible_walls(maze, logo,
                                                      max_x, max_y, n)) < 2:
                    return
                cell.west = False
                n.east = False

    @staticmethod
    def add_solutions(maze: list[list[Optional[Cell]]], logo: list[Cell],
                      max_x: int, max_y: int, entry: tuple[int, int],
                      exit: tuple[int, int]) -> None:
        width, height = (max_x + 1, max_y + 1)

        entry_cell = maze[entry[1]][entry[0]]
        exit_cell = maze[exit[1]][exit[0]]

        WallBuilder.open_all_walls(maze, logo, max_x, max_y, entry_cell)
        WallBuilder.open_all_walls(maze, logo, max_x, max_y, exit_cell)

        n = int(width * height * 0.5)
        for i in range(n):
            rand_x, rand_y = (randint(0, max_x), randint(0, max_y))
            WallBuilder.open_single_wall(maze, logo, max_x,
                                         max_y, maze[rand_y][rand_x])
