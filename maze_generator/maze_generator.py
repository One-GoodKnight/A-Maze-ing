from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Self, ClassVar
from .cell import Cell
from .shape_mazester import ShapeMazester

class MazeGenerator(BaseModel):
    MAX_SIZE: ClassVar = 1000

    width: int = Field(ge=1, le=MAX_SIZE)
    height: int = Field(ge=1, le=MAX_SIZE)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)

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

    # check entry != exit

    def build_maze(self, logo: list[Cell]) -> list[list[Cell]]:
        maze: list[list[Cell]] = ShapeMazester.generate_maze(self.width, self.height, self.entry, self.exit, logo)
        return maze

    def build_output(self, maze: list[list[Cell]]) -> None:
        with open(self.output_file, 'w') as f:
            for row in maze:
                for cell in row:
                    f.write(cell.to_hex())
                f.write("\n")
            f.write("\n")
            f.write(str(self.entry[0]) + ',' + str(self.entry[1]))
            f.write("\n")
            f.write(str(self.exit[0]) + ',' + str(self.exit[1]))
            f.write("\n")
            f.write("temp(should be the solution to the maze)")
