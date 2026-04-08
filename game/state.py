from enum import Enum

class State(Enum):
    INIT = 'init',
    GENERATION = 'generation',
    PLAY = 'play',
    END = 'end'
