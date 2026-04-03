from typing import Optional, Tuple
from random import randint, choice
from .cell import Cell, Direction

class WilsonAlgo():
        @staticmethod
        def rand_pos(max_x, max_y) -> tuple[int, int]:
            return (randint(0, max_x), randint(0, max_y))

        @staticmethod
        def create_starting_walk_cell(maze: list[list[Cell]], max_width: int, max_height: int) -> Cell:
            start = WilsonAlgo.rand_pos(max_width, max_height)
            x, y = start
            while (True):
                if (not maze[y][x]):
                    return Cell(x=x, y=y, north=y==0, east=x==max_width, south=y==max_height, west=x==0)
                else:
                    start = WilsonAlgo.rand_pos(max_width, max_height)
                    x, y = start

        @staticmethod
        def get_close_pos(cell: Cell, dir: Direction) -> list[int, int]:
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
            return (cell.x + offset[0], cell.y + offset[1])

        @staticmethod
        def get_next_cell(maze: list[list[Cell]], cur_cell: Cell, max_width: int, max_height: int) -> Optional[Tuple[Cell, Direction]]:
            directions_checked = {
                'north': cur_cell.north,
                'east': cur_cell.east,
                'south': cur_cell.south,
                'west': cur_cell.west
            }
            while (not all([flag for flag in directions_checked.values()])):
                direction = choice([dir for dir, b in directions_checked.items() if not b])
                directions_checked[direction] = True
                x, y = WilsonAlgo.get_close_pos(cur_cell, direction)
                if (x < 0 or x > max_width or y < 0 or y > max_height):
                    continue
                return (Cell(x=x, y=y, north=y==0, east=x==max_width, south=y==max_height, west=x==0), direction)
            return None

        @staticmethod
        def create_walk(maze: list[list[Cell]], max_width: int, max_height: int) -> list[Cell]:
            walk: list[Cell] = []
            length = 0

            walk.append(WilsonAlgo.create_starting_walk_cell(maze, max_width, max_height))
            cur_cell = walk[0]
            
            while (True):
                next_cell_data = WilsonAlgo.get_next_cell(maze, cur_cell, max_width, max_height)

                if (not next_cell_data):
                    return walk

                next_cell, next_cell_direction = next_cell_data

                if (maze[next_cell.y][next_cell.x]):
                    # next cell is already in maze, we can return the current path
                    walk.append(next_cell)
                    return walk
                elif (next_cell in walk):
                    # next cell is in the current walk, we go back and set the wall of the previous cell to block the path to this cell
                    setattr(cur_cell, next_cell_direction, True)
                    if (cur_cell.isolated()):
                        if (len(walk) == 1):
                            return walk
                        if (walk[-2].x < walk[-1].x):
                            walk[-2].east = True
                        elif (walk[-2].x > walk[-1].x):
                            walk[-2].west = True
                        elif (walk[-2].y < walk[-1].y):
                            walk[-2].south = True
                        elif (walk[-2].y > walk[-1].y):
                            walk[-2].north = True
                        walk.pop()
                        cur_cell = walk[-1]
                else:
                    cur_cell = next_cell
                    walk.append(next_cell)

            # dead end for all the possible paths, should not happen with this algo
            return walk

        @staticmethod
        def add_walk_to_maze(maze: list[list[Optional[Cell]]], walk: list[Cell]) -> int:
            count = 0
            for i, cell in enumerate(walk):
                if (cell == walk[-1] and maze[cell.y][cell.x]):
                    # end of walk is an existing cell of the maze, don't add it
                    maze_cell = maze[cell.y][cell.x]
                    if (walk[i - 1].x < walk[i].x):
                        maze_cell.west = False
                        walk[i - 1].east = False
                    elif (walk[i - 1].x > walk[i].x):
                        maze_cell.east = False
                        walk[i - 1].west = False
                    elif (walk[i - 1].y < walk[i].y):
                        maze_cell.north = False
                        walk[i - 1].south = False
                    elif (walk[i - 1].y > walk[i].y):
                        maze_cell.south = False
                        walk[i - 1].north = False
                    continue
                else:
                    # direction
                    cell.north = True
                    cell.east = True
                    cell.south = True
                    cell.west = True
                    maze[cell.y][cell.x] = cell
                    count += 1
                    if (i == 0):
                        continue
                    if (walk[i - 1].x < cell.x):
                        cell.west = False
                        walk[i - 1].east = False
                    elif (walk[i - 1].x > cell.x):
                        cell.east = False
                        walk[i - 1].west = False
                    elif (walk[i - 1].y < cell.y):
                        cell.north = False
                        walk[i - 1].south = False
                    elif (walk[i - 1].y > cell.y):
                        cell.south = False
                        walk[i - 1].north = False
            return count

        @staticmethod
        def wilson_algo(width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> list[list[Cell]]:
            maze: list[list[Optional[Cell]]] = [[None] * width for _ in range(height)]
            total = 0
            total_target = width * height
            while (total != total_target):
                walk: list[Cell] = WilsonAlgo.create_walk(maze, width - 1, height - 1)
                cells_added = WilsonAlgo.add_walk_to_maze(maze, walk)
                total += cells_added
            return maze
