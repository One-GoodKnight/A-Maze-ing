from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Self, Generator
from .cell import Cell
from .shape_mazester import ShapeMazester
from constants import MAX_MAZE_SIZE


class MazeGenerator(BaseModel):
    width: int = Field(ge=1, le=MAX_MAZE_SIZE)
    height: int = Field(ge=1, le=MAX_MAZE_SIZE)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)
    gen: Generator[list[list[Cell | None]]] | None = Field(default=None)

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

    @model_validator(mode='after')
    def check_entry_eq_exit(self) -> Self:
        if (self.entry[0] == self.exit[0] and self.entry[1] == self.exit[1]):
            raise ValueError("Exit and entry should not be at the same cell")
        return self

    def get_maze_generator(self, logo: list[Cell]
                           ) -> Generator[list[list[Cell]], None, None]:
        maze_generator: list[list[Cell]] = ShapeMazester.maze_generator(
            self.width, self.height, self.entry, self.exit, logo, self.perfect
        )
        return maze_generator

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
