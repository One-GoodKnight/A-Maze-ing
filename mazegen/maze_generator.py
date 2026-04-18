from pydantic import BaseModel, Field, model_validator
from typing import Self, Generator, ClassVar, Any, cast
from .cell import Cell
from .shape_mazester.shape_mazester import ShapeMazester
from .shape_mazester.shapes import Shape
from .solver import solve
from .parsing import parse_config_file
import random


class MazeGenerator(BaseModel):
    """
    Represents a MazeGenerator.

    Attributes:
        MAX_MAZE_SIZE (int): Max width and height of the maze.
        width (int): Width of the maze.
        height (int): Height of the maze.
        entry (tuple[int, int]): Entry of the maze.
        exit (tuple[int, int]): Exit of the maze.
        output_file (str): Output file for the maze and solution.
        perfect (bool): Bool for perfect maze (unique solution).
        shape (Shape): Shape for the maze generation algo.
        gen (Generator[list[list[Cell | None]]]): Gen for the generation.
    """
    MAX_MAZE_SIZE: ClassVar[int] = 50

    width: int = Field(ge=1, le=MAX_MAZE_SIZE)
    height: int = Field(ge=1, le=MAX_MAZE_SIZE)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)
    shape: Shape = Field(default=Shape.CIRCLE)
    gen: Generator[
        list[list[Cell | None]] | bool, None, None
    ] | None = Field(default=None)

    @model_validator(mode='after')
    def check_entry(self) -> Self:
        """Validates entry inside maze."""
        if not ((0 <= self.entry[0] <= self.width - 1) and
                (0 <= self.entry[1] <= self.height - 1)):
            raise ValueError("Entry should be inside the map")
        return self

    @model_validator(mode='after')
    def check_exit(self) -> Self:
        """Validates exit inside maze."""
        if not ((0 <= self.exit[0] <= self.width - 1) and
                (0 <= self.exit[1] <= self.height - 1)):
            raise ValueError("Exit should be inside the map")
        return self

    @model_validator(mode='after')
    def check_entry_eq_exit(self) -> Self:
        """Validates entry on exit."""
        if (self.entry[0] == self.exit[0] and self.entry[1] == self.exit[1]):
            raise ValueError("Exit and entry should not be at the same cell")
        return self

    @classmethod
    def from_file(cls, filename: str) -> "MazeGenerator":
        """
        Creates a MazeGenerator by parsing the config file in the arg.

        Args:
            filename (str): Name of the config file.

        Returns:
            MazeGenerator: The maze generator created from the config file.
        """
        config = parse_config_file(filename)
        random.seed(config['seed'])
        return MazeGenerator(**config)

    def to_dict(self) -> dict[str, Any]:
        """Returns a dict with attrinutes of the class."""
        return {
            'width': self.width,
            'height': self.height,
            'entry': self.entry,
            'exit': self.exit,
            'output_file': self.output_file,
            'perfect': self.perfect,
        }

    def generate_full_maze(self) -> list[list[Cell]]:
        """Returns a complete maze by calling self.gen
        till it returns False."""
        gen: Generator[
            list[list[Cell | None]] | bool, None, None
        ] = self.get_maze_generator([])
        maze: list[list[Cell | None]] = []
        new_maze: list[list[Cell | None]] | bool
        new_maze = next(gen)
        while new_maze:
            maze = cast(list[list[Cell | None]], new_maze)
            new_maze = next(gen)
        return cast(list[list[Cell]], maze)

    def get_solution(self, maze: list[list[Cell]]) -> str:
        """
        Returns a solution to the maze.

        Attributes:
            maze (list[list[Cell]]): Maze to calculate the solution for.

        Returns:
            str: The shortest solution to the maze.
        """
        return solve(maze, self.entry, self.exit)

    def chose_shape(self, shape: str) -> None:
        """
        Sets the shape of the gen for the maze generation algo.

        Attributes:
            shape (str): Shape wanted, see Shape enum for all shapes available.
        """
        for s in Shape:
            if s.value == shape:
                self.shape = s

    def change_seed(self, seed: int) -> None:
        """Changes the seed for the random package."""
        if not isinstance(seed, int):
            return
        random.seed(seed)

    def get_maze_generator(
        self,
        logo: list[Cell]
    ) -> Generator[list[list[Cell | None]] | bool, None, None]:
        """Returns a gen for the maze generation."""
        maze_generator: Generator[
            list[list[Cell | None]] | bool, None, None
        ] = ShapeMazester.maze_generator(
            self.width, self.height, self.entry,
            self.exit, logo, self.perfect, self.shape
        )
        return maze_generator

    def build_output(self, maze: list[list[Cell]]) -> None:
        """
        Writes the maze and a solution to the file self.output_file.

        Attributes:
            maze (list[list[Cell]]): Maze for which we build the output.
        """
        with open(self.output_file, 'w') as f:
            for row in maze:
                for cell in row:
                    f.write(cell.to_hex())
                f.write("\n")
            f.write("\n")
            f.write(str(self.entry[0]) + ',' + str(self.entry[1]) + '\n')
            f.write(str(self.exit[0]) + ',' + str(self.exit[1]) + '\n')
            f.write(solve(maze, self.entry, self.exit) + '\n')
