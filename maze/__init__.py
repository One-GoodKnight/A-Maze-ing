__version__ = "1.0.0"
__author__ = "Nifogi"

from .maze import Maze
from .parsing import parse_config_file

__all__ = [
    "__version__",
    "__author__",
    "Maze",
    "parse_config_file"
]
