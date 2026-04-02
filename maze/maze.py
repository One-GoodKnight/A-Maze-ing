from pydantic import BaseModel, Field, model_validator
from typing import Self, ClassVar
from maze_generator.cell import Cell

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
<<<<<<< HEAD
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
=======
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
>>>>>>> refs/remotes/origin/main
            return Maze(maze=maze, solution=solution, width=width,
                        height=len(maze), entry=entry, exit=exit,
                        output_file=filename)

    def __str__(self) -> str:
<<<<<<< HEAD
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
=======
        chars: list[str] = ["🬕🬂🬂🬨","▌  ▐","🬲🬭🬭🬷"]
        ret: str = ''
        for row in self.maze:
            top = bot = ' '
            for cell in row:
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
>>>>>>> refs/remotes/origin/main
        return ret

    def __repr__(self) -> str:
        ret: str = ''
<<<<<<< HEAD
        for line in self.maze:
            for byte in line:
                ret += byte.to_hex()
=======
        for row in self.maze:
            for cell in row:
                ret += cell.to_hex()
>>>>>>> refs/remotes/origin/main
            ret += '\n'
        return ret
