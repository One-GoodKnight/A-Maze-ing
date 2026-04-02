from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Self, ClassVar
from .cell import Cell
from .wilson_algo import WilsonAlgo

class MazeGenerator(BaseModel):
    MAX_SIZE: ClassVar = 100

    width: int = Field(ge=1, le=MAX_SIZE)
    height: int = Field(ge=1, le=MAX_SIZE)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
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

    def build_output(self) -> None:
        maze: list[list[Cell]] = WilsonAlgo.wilson_algo(self.width, self.height, self.entry, self.height)
        print(maze)
        with open(self.output_file, 'w') as f:
            for row in maze:
                for cell in row:
                    f.write(cell.to_hex())
