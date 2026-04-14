from typing import Self
from collections.abc import Callable
from .cell import Cell


class Node:
    def __init__(self, cell: Cell, g: int, h: int,
                 parent: Self | None = None) -> None:
        self.cell = cell
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    @property
    def x(self) -> int:
        return self.cell.x

    @property
    def y(self) -> int:
        return self.cell.y

    def __eq__(self, cell: Cell) -> bool:
        if cell == self.cell:
            return True
        return False


class AStar:
    def __init__(self, maze: list[list[Cell]], entry: tuple[int, int],
                 exit: tuple[int, int]) -> None:
        self.maze = maze
        self.width = len(maze[0])
        self.height = len(maze)
        self.start: Cell = maze[entry[1]][entry[0]]
        self.goal: Cell = maze[exit[1]][exit[0]]
        self.h: Callable[[Cell, Cell], int] = Cell.manhattan_distance
        self.open_list: list[Node] = [
            Node(self.start, 0, self.h(self.start, self.goal), None)
        ]
        self.closed_list: list[Node] = []

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        x, y = (cell.x, cell.y)
        if not cell.north and y - 1 >= 0:
            neighbors.append(self.maze[y - 1][x])
        if not cell.east and x + 1 < self.width:
            neighbors.append(self.maze[y][x + 1])
        if not cell.south and y + 1 < self.height:
            neighbors.append(self.maze[y + 1][x])
        if not cell.west and x - 1 >= 0:
            neighbors.append(self.maze[y][x - 1])
        return neighbors

    def get_neighbors_node(self, maze: list[list[Cell]],
                           current: Node) -> list[Node]:
        neighbors: list[Node] = []
        neighboring_cells: list[Cell] = self.get_neighbors(current.cell)
        for neighbor in neighboring_cells:
            neighbors.append(
                Node(neighbor, current.g + 1, self.h(current.cell, self.goal))
            )
        return neighbors

    def reconstruct_path(self, current: Node) -> str:
        path = ''
        while current.parent is not None:
            c = current
            p = c.parent
            if c.x == p.x and c.y < p.y:
                path += 'N'
            elif c.x == p.x and c.y > p.y:
                path += 'S'
            elif c.y == p.y and c.x < p.x:
                path += 'W'
            elif c.y == p.y and c.x > p.x:
                path += 'E'
            else:
                raise ValueError("Invalid maze solution")
            current = p
        return path[::-1]

    def run(self) -> str:
        while len(self.open_list) > 0:
            self.open_list.sort(key=lambda x: x.f)
            current = self.open_list.pop(0)
            if current.cell == self.goal:
                return self.reconstruct_path(current)
            self.closed_list.append(current)
            for neighbor in self.get_neighbors_node(self.maze, current):
                if neighbor in self.closed_list:
                    continue
                if neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                neighbor.parent = current
        return ''


def solve(maze: list[list[Cell]], entry: tuple[int, int],
          exit: tuple[int, int]) -> str:
    algo = AStar(maze, entry, exit)
    solution = algo.run()
    return solution
