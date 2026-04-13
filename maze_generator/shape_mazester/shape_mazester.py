import math
from random import randint, choice
from typing import Optional, Tuple
from collections.abc import Generator
from ..cell import Cell
from ..directions import Direction
from .wall_builder import WallBuilder
from .raycast import RayCast
from .shapes import Shape


class ShapeMazester():
    @staticmethod
    def neighbors(maze: list[list[Optional[Cell]]], cell: Cell,
                  max_x: int, max_y: int) -> list[Tuple[int, int, Direction]]:
        if not cell:
            return []
        neighbor_positions = [
            (cell.x, cell.y - 1, Direction.NORTH),
            (cell.x + 1, cell.y, Direction.EAST),
            (cell.x, cell.y + 1, Direction.SOUTH),
            (cell.x - 1, cell.y, Direction.WEST)
        ]
        neighbor_positions = [
            pos for pos in neighbor_positions if
            pos[0] >= 0 and pos[0] <= max_x and
            pos[1] >= 0 and pos[1] <= max_y
        ]

        return neighbor_positions

    @staticmethod
    def empty_neighbors(maze: list[list[Optional[Cell]]], cell: Cell,
                        max_x: int, max_y: int, logo: list[Cell]
                        ) -> Tuple[int, int, Direction]:
        logo_set = {(c.x, c.y) for c in logo}

        neighbor_positions = ShapeMazester.neighbors(maze, cell, max_x, max_y)
        neighbor_positions = [
            pos for pos in neighbor_positions if
            not maze[pos[1]][pos[0]] and
            (pos[0], pos[1]) not in logo_set
        ]
        return neighbor_positions

    @staticmethod
    def find_valid_cell_in_raycast(maze: list[list[Optional[Cell]]],
                                   raycast: list[Tuple[int, int]],
                                   cells: list[Cell], logo: list[Cell]
                                   ) -> Optional[Cell]:
        logo_set = {(c.x, c.y) for c in logo}
        # add randomness to the algo by searching randomly from
        # the end or from the start of the rayscast.
        # prioritizes border towards center to help the algo get
        # the shape wanted but still fill the inside of the maze.
        towards_center = randint(0, 2)

        # iterating the raycast from border to point
        if towards_center > 0:
            for i in range(len(raycast) - 2, -1, -1):
                cell = raycast[i]
                if (cell[0], cell[1]) in logo_set:
                    break

                if not maze[cell[1]][cell[0]]:
                    last_cell_pos = raycast[i + 1]
                    last_cell = maze[last_cell_pos[1]][last_cell_pos[0]]
                    if last_cell:
                        return last_cell

        # no valid cell found, trying in the other direction
        for i in range(1, len(raycast)):
            cell = raycast[i]
            if (cell[0], cell[1]) in logo_set:
                break

            if not maze[cell[1]][cell[0]]:
                last_cell = raycast[i - 1]
                return maze[last_cell[1]][last_cell[0]]

        return None

    def find_valid_neighbor_from_raycast(maze: list[list[Optional[Cell]]],
                                         max_x: int, max_y: int,
                                         raycast: list[Tuple[int, int]],
                                         logo: list[Cell]) -> Optional[Cell]:
        for i in range(len(raycast)):
            pos = (raycast[i][0], raycast[i][1])
            cell = maze[pos[1]][pos[0]]
            neighbors = ShapeMazester.neighbors(maze, cell, max_x, max_y)
            for neighbor in neighbors:
                neighbor_cell = maze[neighbor[1]][neighbor[0]]
                if not neighbor_cell:
                    continue
                if len(ShapeMazester.empty_neighbors(maze, neighbor_cell,
                                                     max_x, max_y, logo)) != 0:
                    return neighbor_cell
        return None

    @staticmethod
    def pick_cell(maze: list[list[Optional[Cell]]], cells: list[Cell],
                  max_x: int, max_y: int,
                  shape_gen: Generator[Tuple[float, float], None, None],
                  start: Tuple[int, int], logo: list[Cell], stuck: bool
                  ) -> Tuple[Optional[Cell], list[Tuple[int, int, float]]]:
        angle = next(shape_gen)
        raycast = RayCast.cast_ray((start[0], start[1]),
                                   next(shape_gen), max_x, max_y)

        cell = ShapeMazester.find_valid_cell_in_raycast(maze, raycast,
                                                        cells, logo)
        if cell:
            return (cell, raycast, angle)

        # no reachable valid cell found,
        # checking neighbors of each cell of the raycast
        cell = ShapeMazester.find_valid_neighbor_from_raycast(
            maze, max_x, max_y, raycast, logo
        )
        if cell:
            return (cell, raycast, angle)

        if not stuck:
            return (None, raycast, angle)

        cell = choice(cells)
        neighbor_positions = ShapeMazester.empty_neighbors(
            maze, cell, max_x, max_y, logo
        )
        while len(neighbor_positions) == 0:
            cell = choice(cells)
            neighbor_positions = ShapeMazester.empty_neighbors(
                maze, cell, max_x, max_y, logo
            )
        return (cell, raycast, angle)

    @staticmethod
    def generate_cell(maze: list[list[Optional[Cell]]],
                      cells: list[Cell], max_x: int, max_y: int,
                      shape_gen: Generator[Tuple[float, float], None, None],
                      start: Tuple[int, int], logo: list[Cell], stuck: bool
                      ) -> Tuple[bool, Optional[list[Tuple[int, int]]], bool]:
        while (True):
            cell, raycast, angle = ShapeMazester.pick_cell(
                maze, cells, max_x, max_y, shape_gen, start, logo, stuck
            )
            try_counter = 0
            while not cell:
                try_counter += 1
                if try_counter >= 1000:
                    stuck = True
                cell, raycast, angle = ShapeMazester.pick_cell(
                    maze, cells, max_x, max_y, shape_gen, start, logo, stuck
                )
            neighbors = ShapeMazester.empty_neighbors(maze, cell,
                                                      max_x, max_y, logo)

            deg_angle = math.degrees(angle)
            # angle goes clockwise, prioritize the direction closest
            # to +90° to follow the curve of the shape
            angle_target = deg_angle + 90
            angle_target %= 360

            direction = None
            if ((angle_target >= 315 and angle_target <= 360) or
                    (angle_target >= 0 and angle_target <= 45)):
                direction = Direction.EAST
            elif (angle_target >= 45 and angle_target <= 135):
                direction = Direction.SOUTH
            elif (angle_target >= 135 and angle_target <= 225):
                direction = Direction.WEST
            else:
                direction = Direction.NORTH

            order = [dir.name for dir in Direction]
            while order[0] != direction.name:
                order.append(order.pop(0))

            while order[0] not in [n[2].name for n in neighbors]:
                order.pop(0)

            while neighbors[0][2].name != order[0]:
                neighbors.pop(0)

            neighbor = neighbors[0]
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
            return (True, raycast, stuck)

    @staticmethod
    def random_starting_pos(max_x: int, max_y: int,
                            logo: list[Cell]) -> Tuple[int, int]:
        logo_set = {(c.x, c.y) for c in logo}

        min_rand_x, max_rand_x = (max_x // 4 * 1, max_x // 4 * 3)
        min_rand_y, max_rand_y = (max_y // 4 * 1, max_y // 4 * 3)

        rand_pos = (randint(min_rand_x, max_rand_x),
                    randint(min_rand_y, max_rand_y))
        counter = 0
        while rand_pos in logo_set:
            rand_pos = (randint(min_rand_x, max_rand_x),
                        randint(min_rand_y, max_rand_y))
            counter += 1
            if counter == 100:
                return (0, 0)
        return (rand_pos)

    @staticmethod
    def maze_generator(width: int, height: int, entry: tuple[int, int],
                       exit: tuple[int, int], logo: list[Cell],
                       perfect: bool, shape: Shape
                       ) -> Generator[list[list[Cell]], None, None]:
        max_x = width - 1
        max_y = height - 1

        shape_gen = shape.get_func()()

        maze: list[list[Optional[Cell]]] = [
            [None] * width for _ in range(height)
        ]
        cells: list[Cell] = []

        start = ShapeMazester.random_starting_pos(max_x, max_y, logo)
        cells.append(Cell(x=start[0], y=start[1]))
        maze[start[1]][start[0]] = cells[0]
        yield maze

        cells_count = 1
        max_cells_count = width * height - len(logo)
        stuck = False

        while (cells_count != max_cells_count):
            (generated, raycast, stuck) = ShapeMazester.generate_cell(
                maze, cells, max_x, max_y, shape_gen, start, logo, stuck
            )
            while (not generated):
                (generated, raycast, stuck) = ShapeMazester.generate_cell(
                    maze, cells, max_x, max_y, shape_gen, start, logo, stuck
                )
            ShapeMazester.toggle_raycast(maze, raycast, True)
            yield maze
            ShapeMazester.toggle_raycast(maze, raycast, False)
            cells_count += 1

        yield maze

        ShapeMazester.add_logo(maze, logo, cells_count)
        WallBuilder.build_wall(maze)
        if not perfect:
            WallBuilder.add_solutions(maze, logo, max_x, max_y, entry, exit)

        yield False

    @staticmethod
    def add_logo(maze: list[list[Optional[Cell]]],
                 logo: list[Cell], cells_count: int) -> None:
        for cell in logo:
            maze[cell.y][cell.x] = cell

    @staticmethod
    def toggle_raycast(maze: list[list[Optional[Cell]]],
                       raycast: Optional[list[Tuple[int, int]]],
                       on: bool) -> None:
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
