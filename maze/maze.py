from pydantic import BaseModel, Field, model_validator
from typing import Self, cast
from maze_generator import Cell
from constants import DEFAULT_CELL_SIZE


class Maze(BaseModel):
    maze: list[list[Cell | None]] | None = Field(default=None)
    solution: str = Field(default='')
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)
    cell_size: int = Field(default=DEFAULT_CELL_SIZE)
    cell_counter: int = Field(default=0)
    init_time: float = 0

    player_solution: str = Field(default='')
    show_solutions: bool = Field(default=False)

    @model_validator(mode='after')
    def check_entry(self) -> Self:
        if not ((0 <= self.entry[0] <= self.width - 1) and
                (0 <= self.entry[1] <= self.height - 1)):
            raise ValueError("Entry should be inside the map")
        return self

    @model_validator(mode='after')
    def check_exit(self) -> Self:
        if not ((0 <= self.exit[0] <= self.width - 1) and
                (0 <= self.exit[1] <= self.height - 1)):
            raise ValueError("Exit should be inside the map")
        return self

    def pixel_to_cell(self, x: int, y: int) -> Cell:
        cell_x: int = x // self.cell_size
        cell_y: int = y // self.cell_size
        return Cell(x=cell_x, y=cell_y)

    def get_entry(self) -> Cell | None:
        if self.maze is not None:
            return self.maze[self.entry[0]][self.entry[1]]
        return None

    def get_exit(self) -> Cell | None:
        if self.maze is not None:
            return self.maze[self.exit[0]][self.exit[1]]
        return None

    def __getitem__(self, index: int) -> list[Cell | None] | None:
        if self.maze is not None:
            return self.maze[index]
        return None

    def __str__(self) -> str:
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
        ret: str = ''
        maze = cast(list[list[Cell]], self.maze)
        for row in maze:
            for cell in row:
                ret += cell.to_hex()
            ret += '\n'
        return ret
