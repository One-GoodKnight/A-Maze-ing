from maze_generator import Cell
from maze import Maze
from game import Player
from constants import (MAZE_SOLUTION_COLOR, MAZE_BACKGROUND_COLOR,
                       MAZE_PLAYER_SOLUTION_COLOR)
from typing import Optional


def highlight_solution(maze: Maze, player: Optional[Player] = None) -> None:
    if player is None:
        solution: str = maze.solution
        cur_cell: Cell = Cell.from_tuple(maze.entry)
        color = MAZE_SOLUTION_COLOR
    else:
        solution: str = maze.player_solution
        cur_cell: Cell = maze.pixel_to_cell(player.x, player.y)
        color = MAZE_PLAYER_SOLUTION_COLOR
    if len(solution) == 0:
        return
    max_x = maze.width - 1
    max_y = maze.height - 1
    if not maze.show_solutions:
        color = MAZE_BACKGROUND_COLOR
    for char in solution:
        match char:
            case 'N':
                cur_cell.y -= 1
            case 'E':
                cur_cell.x += 1
            case 'S':
                cur_cell.y += 1
            case 'W':
                cur_cell.x -= 1
        if ((cur_cell.x < 0 or cur_cell.x > max_x) or
                (cur_cell.y < 0 or cur_cell.y > max_y)):
            return
        maze[cur_cell.y][cur_cell.x].color = color


def clear_solution(maze: Maze, player: Optional[Player] = None) -> None:
    for row in maze.maze:
        for cell in row:
            cell.color = MAZE_BACKGROUND_COLOR
