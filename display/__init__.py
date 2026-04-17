"""
This module is used to display and operate on images drawn on the Mlx window.
"""

__version__ = "1.0.0"
__author__ = "Nifogi"

from .image import Image
from .maze_display import MazeDisplay
from .player_display import display_player
from .font import Font
from .highlight_solution import highlight_solution, clear_solution
from .set_logo_color import set_logo_color, random_maze_logo_color

__all__ = [
    "__version__",
    "__author__",
    'Image',
    'MazeDisplay',
    'display_player',
    'Font',
    'highlight_solution',
    'clear_solution',
    'set_logo_color',
    'random_maze_logo_color',
]
