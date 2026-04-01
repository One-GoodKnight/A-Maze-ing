from pydantic import BaseModel, Field, model_validator
from typing import Self, ClassVar

class Cell(BaseModel):
    north: bool = Field(default=False)
    east: bool = Field(default=False)
    south: bool = Field(default=False)
    west: bool = Field(default=False)

    @staticmethod
    def from_hex(hex: str) -> Self:
        nb = int(hex, 16)
        north = nb & 1
        east = nb >> 1 & 1
        south = nb >> 2 & 1
        west = nb >> 3 & 1
        return Cell(north=north, east=east, south=south, west=west)

    def to_hex(self) -> str:
        north = int(self.north)
        east = int(self.east) << 1
        south = int(self.south) << 2
        west = int(self.west) << 3
        return f"{(north + east + south + west):X}"

    def __str__(self) -> str:
        return self.to_hex()

    def __repr__(self) -> str:
        return self.to_hex()


class Maze(BaseModel):
    MAX_SIZE: ClassVar = 100

    maze: list[list[Cell]]
    solution: str
    width: int = Field(ge=1, le=MAX_SIZE)
    height: int = Field(ge=1, le=MAX_SIZE)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)

    @model_validator(mode='after')
    def check_entry(self) -> Self:
        if not ((0 <= self.entry[0] <= self.MAX_SIZE-1) and
                (0 <= self.entry[1] <= self.MAX_SIZE-1)):
            raise ValueError("Entry should be inside the map")
        return self

    @model_validator(mode='after')
    def check_exit(self) -> Self:
        if not ((0 <= self.exit[0] <= self.MAX_SIZE-1) and
                (0 <= self.exit[1] <= self.MAX_SIZE-1)):
            raise ValueError("Exit should be inside the map")
        return self

    @staticmethod
    def from_file(filename: str) -> Self:
        maze_str: list[str] = []
        with open(filename, 'r') as f:
            line = f.readline().strip()
            width = len(line)
            while line != '':
                if len(line) != width:
                    raise ValueError("Invalid file content: "
                                     "inconsistent maze line length")
                maze_str.append(line)
                line = f.readline().strip()
            entry: tuple[int, int] = tuple(f.readline().strip().split(','))
            exit: tuple[int, int] = tuple(f.readline().strip().split(','))
            solution = f.readline().strip()
            maze: list[list[Cell]] = [[Cell.from_hex(x) for x in line] for line in maze_str]
            return Maze(maze=maze, solution=solution, width=width,
                        height=len(maze), entry=entry, exit=exit,
                        output_file=filename)

    def __str__(self) -> str:
        ret: str = ''
        for line in self.maze:
            top: str = ' '
            bot: str = ' '
            for byte in line:
                if byte.to_hex() == '0':
                    top += '  '
                    bot += '  '
                elif byte.to_hex() == '1':
                    top += '🭶🭶'
                    bot += '  '
                elif byte.to_hex() == '2':
                    top += ' 🭵'
                    bot += ' 🭵'
                elif byte.to_hex() == '3':
                    top += '🭶🭾'
                    bot += ' 🭵'
                elif byte.to_hex() == '4':
                    top += '  '
                    bot += '🭻🭻'
                elif byte.to_hex() == '5':
                    top += '🭶🭶'
                    bot += '🭻🭻'
                elif byte.to_hex() == '6':
                    top += ' 🭵'
                    bot += '🭻🭿'
                elif byte.to_hex() == '7':
                    top += '🭶🭾'
                    bot += '🭻🭿'
                elif byte.to_hex() == '8':
                    top += '🭰 '
                    bot += '🭰 '
                elif byte.to_hex() == '9':
                    top += '🭽🭶'
                    bot += '🭰 '
                elif byte.to_hex() == 'A':
                    top += '🭰🭵'
                    bot += '🭰🭵'
                elif byte.to_hex() == 'B':
                    top += '🭽🭾'
                    bot += '🭰🭵'
                elif byte.to_hex() == 'C':
                    top += '🭰 '
                    bot += '🭼🭻'
                elif byte.to_hex() == 'D':
                    top += '🭽🭶'
                    bot += '🭼🭻'
                elif byte.to_hex() == 'E':
                    top += '🭰🭵'
                    bot += '🭼🭿'
                elif byte.to_hex() == 'F':
                    top += '🭽🭾'
                    bot += '🭼🭿'
                else:
                    ret += byte.to_hex()
            ret += top + '\n'
            ret += bot + '\n'
        return ret

    def __repr__(self) -> str:
        ret: str = ''
        for line in self.maze:
            for byte in line:
                ret += byte.to_hex()
            ret += '\n'
        return ret
