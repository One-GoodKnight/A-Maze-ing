from mazegen import Cell
from typing import Optional


def parse_logo(
    filename: str, maze_width: int, maze_height: int
) -> Optional[tuple[list[Cell], int, int]]:
    """
    Parses the file in args to get the logo.

    Attributes:
        filename (str): Name of the file ro parse.
        maze_width (int): Width of the maze from MazeGenerator.
        maze_height (int): Height of the maze from MazeGenerator.

    Returns:
        Optional[tuple[list[Cell], int, int]]: None if the file is empty
            or if the logo is too big for the maze, else returns tupple with
            a list of cell for the logo, the width and the height.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If the content of the file is invalid for a logo.
    """
    lines: list[str] = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            lines.append(line.removesuffix('\n'))
    if (len(lines) == 0):
        return None
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
                  ) -> Optional[tuple[list[Cell], int, int]]:
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
