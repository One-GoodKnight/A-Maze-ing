from pydantic import BaseModel, Field, model_validator
from typing import Self, ClassVar

class Maze(BaseModel):
    MAX_SIZE: ClassVar = 100

    maze: list[bytes]
    maze: list[list[tuple[int, int, int, int]]]
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
        maze: list[str] = []
        with open(filename, 'r') as f:
            line = f.readline()
            width = len(line)
            while line.strip() != '':
                if len(line) != width:
                    raise ValueError("Invalid file content: "
                                     "inconsistent maze line length")
                maze.append(line)
                line = f.readline()
            line = f.readline()
