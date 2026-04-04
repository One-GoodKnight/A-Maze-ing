from typing import Dict, Any
from enum import StrEnum

class Key(StrEnum):
    WIDTH       = 'width'
    HEIGHT      = 'height'
    ENTRY       = 'entry'
    EXIT        = 'exit'
    OUTPUT_FILE = 'output_file'
    PERFECT     = 'perfect'

def parse_config_file(filename: str) -> Dict[str, Any]:
    conf = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line[:-1]
            line_split = line.split('=')
            if (len(line_split) != 2):
                raise ValueError("Each line of the config file should have 2 columns separated by an equal")

            try:
                key = Key[line_split[0]]
            except KeyError:
                raise ValueError(f"Invalid key '{line_split[0]}'. Valid keys are {[key.name for key in Key]}")
            if (key in conf):
                raise ValueError(f"Cannot have duplicate keys '{line_split[0]}'")
            value = line_split[1]

            match key:
                case 'width' | 'height':
                    try:
                        conf[key] = int(value)
                    except ValueError:
                        raise ValueError(f"Invalid value for key '{key}', '{value}' should be an int")
                case 'entry' | 'exit':
                    positions = value.split(',')
                    if (len(positions) != 2):
                        raise ValueError(f"Each '{key}' value should have 2 ints separated by a comma")
                    try:
                        pos = positions[0]
                        v1 = int(pos)
                        pos = positions[1]
                        v2 = int(pos)
                    except ValueError:
                        raise ValueError(f"Invalid value for key '{key}', '{pos}' should be an int")
                    conf[key] = (v1, v2)
                case 'output_file':
                    conf[key] = value
                case 'perfect':
                    if (value != "True" and value != "False"):
                        raise ValueError("Perfect value should be 'True' or 'False'")
                    conf[key] = True if value == "True" else False
                case _:
                    raise ValueError("Unexpected file, accepting only: KEY=VALUE")
    return conf
