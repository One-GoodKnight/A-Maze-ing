from typing import Dict, Any

def parse_config_file(filename) -> Dict[str, Any]:
    conf = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line[:-1]
            line_split = line.split('=')
            if (len(line_split) != 2):
                raise ValueError("Each line of the config file should have 2 columns separated by an equal")
            match line_split[0]:
                case 'WIDTH':
                    conf['width'] = int(line_split[1])
                case 'HEIGHT':
                    conf['height'] = int(line_split[1])
                case 'ENTRY':
                    positions = line_split[1].split(',')
                    if (len(positions) != 2):
                        raise ValueError("Each entry value should have 2 numbers separated by a comma")
                    conf['entry'] = (int(positions[0]), positions[1])
                case 'EXIT':
                    positions = line_split[1].split(',')
                    if (len(positions) != 2):
                        raise ValueError("Each exit value should have 2 numbers separated by a comma")
                    conf['exit'] = (int(positions[0]), positions[1])
                case 'OUTPUT_FILE':
                    conf['output_file'] = line_split[1]
                case 'PERFECT':
                    if (line_split[1] != "True" and line_split[1] != "False"):
                        raise ValueError("Perfect value should be 'True' or 'False'")
                    conf['perfect'] = True if line_split[1] == "True" else False
                case _:
                    raise ValueError("Unexpected file, accepting only: KEY=VALUE")
    return conf
