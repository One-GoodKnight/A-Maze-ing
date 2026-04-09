import math
from random import randint, uniform, choice
from typing import Optional, Tuple
from collections.abc import Generator
from .cell import Cell
from .directions import Direction
from .wall_builder import WallBuilder
from .raycast import RayCast

class Circle():
    @staticmethod
    def circle(max_x, max_y) -> Generator[float, None, None]:
        perimeter = (2 * (max_x + max_y + 2))
        step_amount = (2 * math.pi) / perimeter * 5
        step = 0
        while (True):
            yield (step % (2 * math.pi))
            step += step_amount / 2

class ShapeMazester():
    @staticmethod
    def neighbors(maze: list[list[Optional[Cell]]], cell: Cell, max_x: int, max_y: int) -> Tuple[int, int, Direction]:
        neighboring_positions = [
            (cell.x, cell.y - 1, Direction.NORTH),
            (cell.x + 1, cell.y, Direction.EAST),
            (cell.x, cell.y + 1, Direction.SOUTH),
            (cell.x - 1, cell.y, Direction.WEST)
        ]
        neighboring_positions = [
            pos for pos in neighboring_positions if
            pos[0] >= 0 and pos[0] <= max_x and
            pos[1] >= 0 and pos[1] <= max_y
        ]

        return neighboring_positions

    @staticmethod
    def empty_neighbors(maze: list[list[Optional[Cell]]], cell: Cell, max_x: int, max_y: int, logo: list[Cell]) -> Tuple[int, int, Direction]:
        neighbor_positions = ShapeMazester.neighbors(maze, cell, max_x, max_y)
        neighbor_positions = [
            pos for pos in neighbor_positions if
            not maze[pos[1]][pos[0]] and
            Cell(x=pos[0], y=pos[1]) not in logo
        ]
        return neighbor_positions

    @staticmethod
    def find_valid_cell_in_raycast(maze: list[list[Optional[Cell]]], raycast: list[Tuple[int, int]], cells: list[Cell], logo: list[Cell]) -> Optional[Cell]:
        for i in range(1, len(raycast)):
            cell = raycast[i]
            if Cell(x=cell[0], y=cell[1]) in logo:
                return None

            if not maze[cell[1]][cell[0]]:
                last_cell = raycast[i - 1]
                return maze[last_cell[1]][last_cell[0]]

        # no valid cell found, trying in the other direction
        for i in range(len(raycast) - 2, -1, -1):
            cell = raycast[i]
            if Cell(x=cell[0], y=cell[1]) in logo:
                return None

            if not maze[cell[1]][cell[0]]:
                last_cell = raycast[i + 1]
                return maze[last_cell[1]][last_cell[0]]

        return None

    def find_valid_neighbor_from_raycast(maze: list[list[Optional[Cell]]], max_x: int, max_y: int, raycast: list[Tuple[int, int]], logo: list[Cell]) -> Optional[Cell]:
        for i in range(len(raycast)):
            pos = (raycast[i][0], raycast[i][1])
            cell = maze[pos[1]][pos[0]]
            neighbors = ShapeMazester.neighbors(maze, cell, max_x, max_y)
            for neighbor in neighbors:
                neighbor_cell = maze[neighbor[1]][neighbor[0]]
                if not neighbor_cell:
                    continue
                if len(ShapeMazester.empty_neighbors(maze, neighbor_cell, max_x, max_y, logo)) != 0:
                    return neighbor_cell
            return None

    @staticmethod
    def pick_cell(maze: list[list[Optional[Cell]]], cells: list[Cell], max_x: int, max_y: int, shape_gen: Generator[Tuple[float, float], None, None], exit: Tuple[int, int], logo: list[Cell]) -> Tuple[Optional[Cell], list[Tuple[int, int]]]:
        raycast = RayCast.cast_ray((exit[0], exit[1]), next(shape_gen), max_x, max_y)

        cell = ShapeMazester.find_valid_cell_in_raycast(maze, raycast, cells, logo)
        if cell:
            return (cell, raycast)

        # no reachable valid cell found, checking neighbors of each cell of the raycast
        cell = ShapeMazester.find_valid_neighbor_from_raycast(maze, max_x, max_y, raycast, logo)
        if cell:
            return (cell, raycast)

        cell = choice(cells)
        neighboring_positions = ShapeMazester.empty_neighbors(maze, cell, max_x, max_y, logo)
        while len(neighboring_positions) == 0:
            cell = choice(cells)
            neighboring_positions = ShapeMazester.empty_neighbors(maze, cell, max_x, max_y, logo)
        return (cell, raycast)

    @staticmethod
    def generate_cell(maze: list[list[Optional[Cell]]], cells: list[Cell], max_x: int, max_y: int, shape_gen: Generator[Tuple[float, float], None, None], exit: Tuple[int, int], logo: list[Cell]) -> Tuple[bool, Optional[list[Tuple[int, int]]]]:
        while (True):
            cell, raycast = ShapeMazester.pick_cell(maze, cells, max_x, max_y, shape_gen, exit, logo)
            neighboring_positions = ShapeMazester.empty_neighbors(maze, cell, max_x, max_y, logo)

            neighbor = choice(neighboring_positions)
            new_cell = Cell(x=neighbor[0], y=neighbor[1])
            match neighbor[2]:
                case Direction.NORTH:
                    cell.dir_north = True
                    new_cell.dir_south = True
                case Direction.EAST:
                    cell.dir_east = True
                    new_cell.dir_west = True
                case Direction.SOUTH:
                    cell.dir_south = True
                    new_cell.dir_north = True
                case Direction.WEST:
                    cell.dir_west = True
                    new_cell.dir_east = True
            maze[neighbor[1]][neighbor[0]] = new_cell
            cells.append(new_cell)
            return (True, raycast)

    @staticmethod
    def maze_generator(width: int, height: int, entry: tuple[int, int], exit: tuple[int, int], logo: list[Cell]) -> Generator[list[list[Cell]], None, None]:
        max_x = width - 1
        max_y = height - 1

        shape_gen = Circle.circle(max_x, max_y)

        maze: list[list[Optional[Cell]]] = [[None] * width for _ in range(height)]
        cells: list[Cell] = []

        cells.append(Cell(x=exit[0], y=exit[1]))
        maze[exit[1]][exit[0]] = cells[0]
        WallBuilder.build_wall(maze)
        yield maze

        cells_count = 1
        max_cells_count = width * height - len(logo)
        while (cells_count != max_cells_count):
            (generated, raycast) = ShapeMazester.generate_cell(maze, cells, max_x, max_y, shape_gen, exit, logo)
            while (not generated):
                (generated, raycast) = ShapeMazester.generate_cell(maze, cells, max_x, max_y, shape_gen, exit, logo)
            WallBuilder.build_wall(maze)
            ShapeMazester.toggle_raycast(maze, raycast, True)
            yield maze
            ShapeMazester.toggle_raycast(maze, raycast, False)
            cells_count += 1
            #print(cells_count)

        ShapeMazester.add_logo(maze, logo, cells_count)

        WallBuilder.build_wall(maze)
        yield maze
        yield False

    @staticmethod
    def add_logo(maze: list[list[Optional[Cell]]], logo: list[Cell], cells_count: int) -> None:
        for cell in logo:
            maze[cell.y][cell.x] = cell

    @staticmethod
    def toggle_raycast(maze: list[list[Optional[Cell]]], raycast: Optional[list[Tuple[int, int]]], on: bool) -> None:
        if not raycast:
            return
        if on:
            color = 0xFF_FF_FF_FF
        else:
            color = 0x00_00_00_00
        for pos in raycast:
            cell = maze[pos[1]][pos[0]]
            if cell:
                cell.color = color
