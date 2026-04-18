from mazegen import Cell
from constants import Const
from random import randint


def set_logo_color(logo: list[Cell]) -> None:
    """Set the color of each cell composing the 42 logo."""
    for cell in logo:
        cell.color = Const.LOGO_COLOR


def random_color() -> int:
    """Returns a random color in an ARGB integer representation."""
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
    """Set the logo to a random color."""
    for c in logo:
        maze[c.y][c.x].color = random_color()
