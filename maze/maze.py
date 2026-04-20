from pydantic import BaseModel, Field, model_validator
from typing import Self, cast
from mazegen import Cell
from constants import Const


class Maze(BaseModel):
    """
    Represents a Maze with metadata for the generation and the game

    Attributes:
        maze (list[list[Cell | None]]): Cells of the maze.
        solution (str): Shortest solution from entry to exit.
        width] (int): Width of the maze.
        height (int): Height of the maze.
        entry (tuple[int, int]): Entry of the maze.
        exit (tuple[int, int]): Exit of the maze.
        output_file (str): Name of the file to write the maze to.
        perfect (bool): Maze perfect or not (unique solution if perfect).
        cell_size (int): Size of a cell in pixels.
        cell_counter (int): Number of cells on the maze.
        init_time (float): Metadata for the maze generation,
            time at which the first cell has been generated.
        player_solution (str): Shortest solution from the player to the exit.
        show_solutions (bool): Metadata for the game, tells it to show
            solution or not.
    """
    maze: list[list[Cell | None]] | None = Field(default=None)
    solution: str = Field(default='')
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)
    cell_size: int = Field(default=Const.DEFAULT_CELL_SIZE)
    cell_counter: int = Field(default=0)
    init_time: float = 0

    player_solution: str = Field(default='')
    show_solutions: bool = Field(default=False)

    @model_validator(mode='after')
    def check_entry(self) -> Self:
        """Checks if the entry is inside the map."""
        if not ((0 <= self.entry[0] <= self.width - 1) and
                (0 <= self.entry[1] <= self.height - 1)):
            raise ValueError("Entry should be inside the map")
        return self

    @model_validator(mode='after')
    def check_exit(self) -> Self:
        """Checks if the exit is inside the map."""
        if not ((0 <= self.exit[0] <= self.width - 1) and
                (0 <= self.exit[1] <= self.height - 1)):
            raise ValueError("Exit should be inside the map")
        return self

    def pixel_to_cell(self, x: int, y: int) -> Cell:
        """Returns a new cell with x and y passed as pixel."""
        cell_x: int = x // self.cell_size
        cell_y: int = y // self.cell_size
        return Cell(x=cell_x, y=cell_y)

    def get_entry(self) -> Cell | None:
        """Returns the entry cell of the maze."""
        if self.maze is not None:
            return self.maze[self.entry[0]][self.entry[1]]
        return None

    def get_exit(self) -> Cell | None:
        """Returns the exit cell of the maze."""
        if self.maze is not None:
            return self.maze[self.exit[0]][self.exit[1]]
        return None

    def __getitem__(self, index: int) -> list[Cell | None] | None:
        """Returns a row of the maze"""
        if self.maze is not None:
            return self.maze[index]
        return None

    @staticmethod
    def from_file(filename: str) -> Self:
        maze_str: list[str] = []
        with open(filename, 'r') as f:
            row = f.readline().strip()
            width = len(row)
            while row != '':
                if len(row) != width:
                    raise ValueError("Invalid file content: "
                                     "inconsistent maze row length")
                maze_str.append(row)
                row = f.readline().strip()
            entry: tuple[int, int] = tuple(f.readline().strip().split(','))
            exit: tuple[int, int] = tuple(f.readline().strip().split(','))
            solution = f.readline().strip()
            maze = [
                [Cell.from_hex(c, x, y) for x, c in enumerate(row)]
                for y, row in enumerate(maze_str)
            ]
            maze[int(entry[1])][int(entry[0])].color = 0xFF_00_FF_00
            maze[int(exit[1])][int(exit[0])].color = 0xFF_FF_00_00
            return Maze(maze=maze, solution=solution, width=width,
                        height=len(maze), entry=entry, exit=exit,
                        output_file=filename)

    def __str__(self) -> str:
        """Returns the maze in ASCII art."""
        chars: list[str] = ["🬕🬂🬂🬨", "▌  ▐", "🬲🬭🬭🬷"]
        ret: str = ''
        for row in self.maze if self.maze is not None else []:
            top = bot = ' '
            for cell in row:
                if not cell:
                    continue
                top_left = top_right = bot_left = bot_right = '  '
                if cell.north:
                    if cell.west:
                        top_left = chars[0][:2]
                    else:
                        top_left = chars[0][1:3]
                    if cell.east:
                        top_right = chars[0][2:]
                    else:
                        top_right = chars[0][1:3]
                else:
                    if cell.west:
                        top_left = chars[1][:2]
                    if cell.east:
                        top_right = chars[1][2:]
                if cell.south:
                    if cell.west:
                        bot_left = chars[2][:2]
                    else:
                        bot_left = chars[2][1:3]
                    if cell.east:
                        bot_right = chars[2][2:]
                    else:
                        bot_right = chars[2][1:3]
                else:
                    if cell.west:
                        bot_left = chars[1][:2]
                    if cell.east:
                        bot_right = chars[1][2:]
                top += top_left + top_right
                bot += bot_left + bot_right
            ret += top + '\n' + bot + '\n'
        return ret

    def __repr__(self) -> str:
        """Returns the maze in hexadecimal string format with a line for
        each row."""
        ret: str = ''
        maze = cast(list[list[Cell]], self.maze)
        for row in maze:
            for cell in row:
                ret += cell.to_hex()
            ret += '\n'
        return ret
