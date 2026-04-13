from enum import Enum


class State(Enum):
    INIT_GENERATION = 'init_generation',
    GENERATION = 'generation',
    INIT_PLAY = 'init_play',
    PLAY = 'play',
    END = 'end'
