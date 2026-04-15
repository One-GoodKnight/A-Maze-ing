from maze_generator import Cell
from constants import LOGO_COLOR
from random import randint


def set_logo_color(logo: list[Cell]) -> None:
    for cell in logo:
        cell.color = LOGO_COLOR


def random_color() -> int:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (
        0xFF << 24 |
        r << 16 |
        g << 8 |
        b
    )


def random_maze_logo_color(maze: list[list[Cell]], logo: list[Cell]) -> None:
    for c in logo:
        maze[c.y][c.x].color = random_color()
