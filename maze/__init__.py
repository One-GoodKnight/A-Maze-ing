__version__ = "1.0.0"
__author__ = "Nifogi"

from .maze_generator import MazeGenerator
from .parsing import parse_config_file
from .maze import Maze

__all__ = [
    "__version__",
    "__author__",
    "Maze"
    "MazeGenerator",
    "parse_config_file"
]
