"""
Maze generation.

This pakage provides a class MazeGenerator with methods
to parse a config file, create a maze and find
a solution to this maze.
"""


__version__ = "1.0.0"
__author__ = "Nifogi"

from .maze_generator import MazeGenerator
from .cell import Cell
from .shape_mazester.wall_builder import WallBuilder
from .shape_mazester.directions import Direction
from .shape_mazester.shapes import Shape
from .solver import solve

__all__ = [
    "__version__",
    "__author__",
    "MazeGenerator",
    "Cell",
    "WallBuilder",
    "Direction",
    "Shape",
    "solve",
]
