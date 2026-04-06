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
        step_amount = (2 * math.pi) / perimeter
        step = 0
        while (True):
            yield (step % (2 * math.pi))
            step += step_amount / 2

class ShapeMazester():
    @staticmethod
    def pick_cell(maze: list[list[Optional[Cell]]], cells: list[Cell], max_x: int, max_y: int, shape_gen: Generator[Tuple[float, float], None, None], raycast_angle: float, entry: Tuple[int, int]) -> Cell:
        cells_in_raycast = RayCast.cast_ray((entry[0], entry[1]), raycast_angle, max_x, max_y)
        for i in range(len(cells_in_raycast) - 1, -1, -1):
            cell = cells_in_raycast[i]
            if (maze[cell[1]][cell[0]]):
                return maze[cell[1]][cell[0]]
        return cells[0]

    @staticmethod
    def available_neighbors(maze: list[list[Optional[Cell]]], cell: Cell, max_x: int, max_y: int, logo: list[Cell]) -> Tuple[int, int, Direction]:
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
        neighboring_positions = [
            pos for pos in neighboring_positions if
            not maze[pos[1]][pos[0]] and
            Cell(x=pos[0], y=pos[1]) not in logo
        ]
        return neighboring_positions

    @staticmethod
    def generate_cell(maze: list[list[Optional[Cell]]], cells: list[Cell], max_x: int, max_y: int, shape_gen: Generator[Tuple[float, float], None, None], entry: Tuple[int, int], logo: list[Cell]) -> None:
        while (True):
            raycast_angle = next(shape_gen)
            cell = ShapeMazester.pick_cell(maze, cells, max_x, max_y, shape_gen, raycast_angle, entry)
            neighboring_positions = ShapeMazester.available_neighbors(maze, cell, max_x, max_y, logo)
            while (len(neighboring_positions) == 0):
                cell = choice(cells)
                neighboring_positions = ShapeMazester.available_neighbors(maze, cell, max_x, max_y, logo)
            angle_deg = math.degrees(raycast_angle)
            if (angle_deg >= -45 and angle_deg <= 45):
                target_direction = Direction.EAST
            elif (angle_deg >= 45 and angle_deg <= 135):
                target_direction = Direction.SOUTH
            elif (angle_deg >= 135 and angle_deg <= 225):
                target_direction = Direction.WEST
            else:
                target_direction = Direction.NORTH

            if (target_direction in [n[2] for n in neighboring_positions]):
                for n in neighboring_positions:
                    if n[2] == target_direction:
                        neighbor = n
            else:
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
            return

    @staticmethod
    def generate_maze(width: int, height: int, entry: tuple[int, int], exit: tuple[int, int], logo: list[Cell]) -> list[list[Cell]]:
        max_x = width - 1
        max_y = height - 1

        shape_gen = Circle.circle(max_x, max_y)

        maze: list[list[Optional[Cell]]] = [[None] * width for _ in range(height)]
        cells: list[Cell] = []

        opposite_exit = (max_x - exit[0], max_y - exit[1])
        cells.append(Cell(x=opposite_exit[0], y=opposite_exit[1]))
        maze[opposite_exit[1]][opposite_exit[0]] = cells[0]

        cells_count = 1
        max_cells_count = width * height - len(logo)
        while (cells_count != max_cells_count):
            ShapeMazester.generate_cell(maze, cells, max_x, max_y, shape_gen, entry, logo)
            cells_count += 1
            #print(cells_count)

        ShapeMazester.add_logo(maze, logo, cells_count)
        ShapeMazester.add_color(maze, entry, exit)
        
        WallBuilder.build_wall(maze)
        return maze

    @staticmethod
    def add_color(maze: list[list[Optional[Cell]]], entry: Tuple[int, int], exit: Tuple[int, int]) -> None:
        maze[entry[1]][entry[0]].color = 0xFF_00_FF_00
        maze[exit[1]][exit[0]].color = 0x_FF_FF_00_00

    @staticmethod
    def add_logo(maze: list[list[Optional[Cell]]], logo: list[Cell], cells_count: int) -> None:
        for cell in logo:
            maze[cell.y][cell.x] = cell
