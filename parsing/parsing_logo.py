from maze_generator import Cell
from typing import Tuple, Optional


def parse_logo(filename: str, maze_width: int, maze_height: int) -> list[Cell]:
    lines: list[str] = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            lines.append(line.removesuffix('\n'))
    if (len(lines) == 0):
        return lines
    width = len(lines[0])
    for line in lines:
        if (len(line) != width):
            raise ValueError("Every size length of the "
                             "logo should be the same.")
    for line in lines:
        for c in line:
            if (c != ' ' and c != 'x'):
                raise ValueError("Only characters allowed "
                                 "in the logo file are ' ' and 'x'")
    height = len(lines)
    return logo_to_cells(lines, width, height, maze_width, maze_height)


def logo_to_cells(lines: list[str], width: int, height: int,
                  maze_width: int, maze_height: int
                  ) -> Optional[Tuple[list[Cell], int, int]]:
    cells: list[Cell] = []
    offset_x, offset_y = (maze_width // 2 - width // 2,
                          maze_height // 2 - height // 2)
    if (offset_x < 0 or offset_y < 0):
        return None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if (c == 'x'):
                cells.append(Cell(x=x + offset_x, y=y + offset_y))
    return (cells, width, height)
