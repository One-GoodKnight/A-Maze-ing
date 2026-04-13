from typing import Self, Optional
from collections.abc import Callable
from maze import Maze
from maze_generator import Cell
from game import Player


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
    def __init__(self, maze: Maze, player: Optional[Player] = None) -> None:
        self.maze = maze
        if player is None:
            self.start: Cell = maze.get_entry()
        else:
            self.start: Cell = maze.pixel_to_cell(player.x, player.y)
        self.goal: Cell = maze.get_exit()
        self.h: Callable[[Cell, Cell], int] = Cell.manhattan_distance
        self.open_list: list[Node] = [
            Node(self.start, 0, self.h(self.start, self.goal), None)
        ]
        self.closed_list: list[Node] = []

    def get_neighbors(self, maze: Maze, current: Node) -> list[Node]:
        neighbors: list[Node] = []
        neighboring_cells: list[Cell] = maze.get_neighbors(current.cell)
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
            for neighbor in self.get_neighbors(self.maze, current):
                if neighbor in self.closed_list:
                    continue
                if neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                neighbor.parent = current
        return ''


def solve(maze: Maze, player: Optional[Player] = None) -> str:
    algo = AStar(maze, player)
    solution = algo.run()
    if player is None:
        maze.solution = solution
    else:
        maze.player_solution = solution
    return solution
