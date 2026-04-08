__version__ = "1.0.0"
__author__ = "Nifogi"

from .game import Game
from .player import Player
from .state import State
from .end import check_end

__all__ = [
    "__version__",
    "__author__",
    'Game',
    'Player',
    'State',
    'check_end'
]
