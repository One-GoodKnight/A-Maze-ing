from enum import Enum


class State(Enum):
    """Simple enum for the states of the game."""
    INIT_GENERATION = 'init_generation',
    GENERATION = 'generation',
    INIT_PLAY = 'init_play',
    PLAY = 'play',
    END = 'end'
