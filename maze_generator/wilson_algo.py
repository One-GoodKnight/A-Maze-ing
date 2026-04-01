from typing import Optional
from random import randint, choice
from .cell import Cell, Direction

class WilsonAlgo():
        @staticmethod
        def rand_pos(max_x, max_y) -> tuple[int, int]:
            return (randint(0, max_x), randint(0, max_y))

        @staticmethod
        def get_close_pos(cur_cell: Cell, dir: Direction) -> list[int, int]:
            offset = [0, 0]
            match (dir):
                case Direction.NORTH:
                    offset[1] -= 1
                case Direction.EAST:
                    offset[0] += 1
                case Direction.SOUTH:
                    offset[1] += 1
                case Direction.WEST:
                    offset[0] -= 1
            return (cur_cell.x + offset[0], cur_cell.y + offset[1])

        @staticmethod
        def get_next_cell_pos(maze: list[list[Cell]], cur_cell: Cell, max_width: int, max_height: int) -> Optional[tuple[int, int, Direction]]:
            checked = {dir: False for dir in list(Direction)}
            while (not all([b for b in checked.values()])):
                dir = choice([dir for dir, b in checked.items() if not b])
                checked[dir] = True
                x, y = WilsonAlgo.get_close_pos(cur_cell, dir)
                if (x < 0 or x > max_width or y < 0 or y > max_height):
                    continue
                #next_cell = Cell(x=x, y=y, **{d: True if d == dir else False for d in list(Direction)})
                return (x, y, dir)
            return None

        @staticmethod
        def cell_has_multiple_exits(cell: Cell):
            pass

        @staticmethod
        def walk(maze: list[list[Cell]], max_width: int, max_height: int) -> int:
            walk: list[list[Cell]] = [[None] * (max_width + 1) for _ in range(max_height + 1)]
            length = 0

            # Starting walk cell
            start = WilsonAlgo.rand_pos(max_width, max_height)
            x, y = start
            start_found = False
            while (not start_found):
                if (not maze[y][x]):
                    maze[y][x] = Cell(x=x, y=y, north=False, east=False, south=False, west=False)
                    length += 1
                    start_found = True
                else:
                    start = WilsonAlgo.rand_pos(max_width, max_height)
                    x, y = start
            cur_cell = maze[y][x]
            
            next_pos = WilsonAlgo.get_next_cell_pos(maze, cur_cell, max_width, max_height)
            last_available_cell = WilsonAlgo.has_cell_multiple_exits()
            while (next_pos):
                if (walk[next_pos[1]][next_pospp[0]]):
                    if (not last_available_cell):
                        print("should not happen")
                        return length
                    cur_cell = last_available_cell
                if (maze[next_pos[1]][next_pos[0]]):
                    # open maze cell wall
                    return length
                length += 1
                dir = next_pos[2]
                cell = Cell(
                    x=next_pos[0],
                    y=next_pos[1],
                    north=(dir==Direction.NORTH),
                    east=(dir==Direction.EAST),
                    south=(dir==Direction.SOUTH),
                    west=(dir==Direction.WEST)
                )
                walk[cell.y][cell.x] = cell
                maze[cell.y][cell.x] = cell
                cur_cell = cell
                if (cell_has_multiple_exits()):
                    last_available_cell = cur_cell
                next_pos = WilsonAlgo.get_next_cell_pos(maze, cur_cell, max_width, max_height)

            return length

        @staticmethod
        def wilson_algo(width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> list[list[Cell]]:
            maze: list[list[Optional[Cell]]] = [[None] * width for _ in range(height)]
            total = 0
            total_target = width * height
            while (total != total_target):
                total += WilsonAlgo.walk(maze, width - 1, height - 1)
            return maze
