from maze_generator import Cell
from .image import Image
from constants import MAZE_SOLUTION_COLOR, MAZE_BACKGROUND_COLOR
from typing import Tuple

def highlight_solution(image: Image, maze: list[list[Cell]], start: Tuple[int, int], solution: str, on: bool = True) -> None:
    if not solution:
        return

    max_x = len(maze[0]) - 1
    max_y = len(maze) - 1

    color = MAZE_SOLUTION_COLOR

    if not on:
        color = MAZE_BACKGROUND_COLOR

    cur_cell: list[int, int] = [start[0], start[1]]

    for c in solution:
        match c:
            case 'N':
                cur_cell[1] -= 1
            case 'E':
                cur_cell[0] += 1
            case 'S':
                cur_cell[1] += 1
            case 'W':
                cur_cell[0] -=1

        if (cur_cell[0] < 0 or cur_cell[0] > max_x):
            return
        if (cur_cell[1] < 0 or cur_cell[1] > max_y):
            return

        maze[cur_cell[1]][cur_cell[0]].color = color


def clear_solution(image: Image, maze: list[list[Cell]], start: Tuple[int, int], solution: str):
    highlight_solution(image, maze, start, solution, False)
