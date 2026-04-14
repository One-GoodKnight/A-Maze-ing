from ..shape_mazester.shapes import Shape
from typing import Dict, Any
from enum import StrEnum


class Key(StrEnum):
    WIDTH = 'width'
    HEIGHT = 'height'
    ENTRY = 'entry'
    EXIT = 'exit'
    OUTPUT_FILE = 'output_file'
    PERFECT = 'perfect'
    SEED = 'seed'
    SHAPE = 'shape'


def parse_config_file(filename: str) -> Dict[str, Any]:
    conf = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.removesuffix('\n')
            if (line.find('#') == 0):
                continue
            line_split = line.split('=')
            if (len(line_split) != 2):
                raise ValueError("Each line of the config file should "
                                 "have 2 columns separated by an equal")

            try:
                key = Key[line_split[0]]
            except KeyError:
                raise ValueError(f"Invalid key '{line_split[0]}'. "
                                 f"Valid keys are {[key.name for key in Key]}")
            if (key in conf):
                raise ValueError("Cannot have duplicate "
                                 f"keys '{line_split[0]}'")
            value = line_split[1]

            match key:
                case 'width' | 'height' | 'seed':
                    try:
                        conf[key] = int(value)
                    except ValueError:
                        raise ValueError(f"Invalid value for key '{key}', "
                                         f"'{value}' should be an int")
                case 'entry' | 'exit':
                    positions = value.split(',')
                    if (len(positions) != 2):
                        raise ValueError(f"Each '{key}' value should "
                                         "have 2 ints separated by a comma")
                    try:
                        pos = positions[0]
                        v1 = int(pos)
                        pos = positions[1]
                        v2 = int(pos)
                    except ValueError:
                        raise ValueError(f"Invalid value for key '{key}', "
                                         f"'{pos}' should be an int")
                    conf[key] = (v1, v2)
                case 'output_file':
                    if len(value) == 0:
                        raise ValueError("Output file name must not be empty")
                    if not value.endswith('.txt'):
                        raise ValueError("Output file name must "
                                         "end with '.txt'")
                    if value.startswith('/'):
                        raise ValueError("Output file name must "
                                         "not start with '/'")
                    if './' in value:
                        raise ValueError("Output file name must "
                                         "not contain './'")
                    conf[key] = value
                case 'perfect':
                    if (value != "True" and value != "False"):
                        raise ValueError("Perfect value should be "
                                         "'True' or 'False'")
                    conf[key] = True if value == "True" else False
                case 'shape':
                    if value not in [shape.value for shape in Shape]:
                        raise ValueError("Invalid shape, valid shapes for "
                                         "the maze generation are: "
                                         f"{[shape.value for shape in Shape]}")
                    conf[key] = value
                case _:
                    raise ValueError("Unexpected file format, "
                                     "accepting only: KEY=VALUE")

    if (set([key.value for key in Key]) != set([key for key in conf.keys()])):
        keys = [key.name for key in Key if key.value not in conf.keys()]
        raise ValueError(f"Missing keys {keys}"
                         ", all keys must be present in the config file "
                         f"{[key.name for key in Key]}")
    return conf
