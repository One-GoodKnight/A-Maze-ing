from mazegen import Cell
from constants import Const
from typing import Tuple, Optional, cast


def highlight_solution(
    maze: list[list[Cell | None]] | None, start: Tuple[int, int],
    solution: str, sol_color: Optional[int], on: bool = True
) -> None:
    """
    Changes the color of every cell in the path of the given solution.

    Args:
        maze (list[list[Cell]]): Grid of cells representing the maze.
        start (tuple(x: int, y: int)): Coordinate of the Cell on which
            the solution starts.
        solution (str): Solution to the given maze. Example: 'WSWWSSSEEN'
        sol_color (int): Color to give to cells in the solution.
        on (bool): Whether the cells should be colored or not. Default to True.
    """
    if not solution or maze is None or maze[0] is None:
        return

    max_x = len(maze[0]) - 1
    max_y = len(maze) - 1

    color = sol_color

    if not on or not sol_color:
        color = Const.MAZE_BACKGROUND_COLOR

    cur_cell: list[int] = [start[0], start[1]]

    for c in solution:
        match c:
            case 'N':
                cur_cell[1] -= 1
            case 'E':
                cur_cell[0] += 1
            case 'S':
                cur_cell[1] += 1
            case 'W':
                cur_cell[0] -= 1

        if (cur_cell[0] < 0 or cur_cell[0] > max_x):
            return
        if (cur_cell[1] < 0 or cur_cell[1] > max_y):
            return

        if color:
            cast(Cell, maze[cur_cell[1]][cur_cell[0]]).color = color


def clear_solution(
    maze: list[list[Cell | None]] | None, start: Tuple[int, int], solution: str
) -> None:
    """
    Set the color of each cells on the solution path to the default color,
    effectively hiding the solution.
    """
    highlight_solution(maze, start, solution, None, False)
