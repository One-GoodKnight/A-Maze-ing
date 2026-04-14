from typing import Self, Optional, Tuple
from collections.abc import Callable
from ..cell import Cell


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
    def __init__(self, maze: list[list[Cell]], entry: Tuple[int, int], exit: Tuple[int, int]) -> None:
        self.maze = maze
        self.start: Cell = maze[entry[1]][entry[0]]
        self.goal: Cell = maze[exit[1]][exit[0]]
        self.h: Callable[[Cell, Cell], int] = Cell.manhattan_distance
        self.open_list: list[Node] = [
            Node(self.start, 0, self.h(self.start, self.goal), None)
        ]
        self.closed_list: list[Node] = []

    @staticmethod
    def get_neighbors(maze: list[list[Cell]], cell: Cell) -> list[Cell]:
        width = len(maze[0])
        height = len(maze)

        neighbors: list[Cell] = []
        x, y = (cell.x, cell.y)
        if not cell.north and y - 1 >= 0:
            neighbors.append(maze[y - 1][x])
        if not cell.east and x + 1 < width:
            neighbors.append(maze[y][x + 1])
        if not cell.south and y + 1 < height:
            neighbors.append(maze[y + 1][x])
        if not cell.west and x - 1 >= 0:
            neighbors.append(maze[y][x - 1])
        return neighbors

    def get_neighbors_node(self, maze: list[list[Cell]], current: Node) -> list[Node]:
        neighbors: list[Node] = []
        neighboring_cells: list[Cell] = AStar.get_neighbors(maze, current.cell)
        for neighbor in neighboring_cells:
            neighbors.append(
                Node(neighbor, current.g + 1, self.h(current.cell, self.goal))
            )
        return neighbors

    def reconstruct_path(self, current: Node) -> str:
        path = ''
        while current.parent is not None:
            if current.x == current.parent.x and current.y < current.parent.y:
                path += 'N'
            elif current.x == current.parent.x and current.y > current.parent.y:
                path += 'S'
            elif current.y == current.parent.y and current.x < current.parent.x:
                path += 'W'
            elif current.y == current.parent.y and current.x > current.parent.x:
                path += 'E'
            else:
                raise ValueError("Invalid maze solution")
            current = current.parent
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


def solve(maze: list[list[Cell]], entry: Tuple[int, int], exit: Tuple[int, int]) -> str:
    algo = AStar(maze, entry, exit)
    solution = algo.run()
    return solution
