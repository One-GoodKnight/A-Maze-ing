from pydantic import BaseModel, Field
from typing import Any


class Cell(BaseModel):
    """
    Represents a cell of mazes.

    Attributes:
        x (int): x pos.
        y (int): y pos.
        north (bool): North wall.
        east (bool): East wall.
        south (bool): South wall.
        west (bool): West wall.
        dir_north (bool): Direction north has a cell and is open.
        dir_east (bool): Direction east has a cell and is open.
        dir_south (bool): Direction south has a cell and is open.
        dir_west (bool): Direction west has a cell and is open.
        color (int): Color of the cell on the display.
    """
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    north: bool = Field(default=False)
    east: bool = Field(default=False)
    south: bool = Field(default=False)
    west: bool = Field(default=False)
    dir_north: bool = Field(default=False)
    dir_east: bool = Field(default=False)
    dir_south: bool = Field(default=False)
    dir_west: bool = Field(default=False)
    color: int = Field(default=0)

    def to_int(self) -> int:
        """Returns an int using the walls of the cell as follow NESW."""
        north = int(self.north)
        east = int(self.east) << 1
        south = int(self.south) << 2
        west = int(self.west) << 3
        return north + east + south + west

    def to_hex(self) -> str:
        """Returns the hex version of the to_int() as str."""
        return f"{self.to_int():X}"

    def isolated(self) -> bool:
        """Returns True if all four walls are True."""
        return (
            self.north and
            self.east and
            self.south and
            self.west
        )

    @staticmethod
    def manhattan_distance(c1: "Cell", c2: "Cell") -> int:
        """Returns the difference x + difference y of two cells as an int."""
        return abs(c1.x - c2.x) + abs(c1.y - c2.y)

    def __eq__(self, other: Any) -> bool:
        """Compares two cells with their x and y values and returns a bool."""
        if not isinstance(other, Cell):
            return False
        return (self.x == other.x and self.y == other.y)

    def __str__(self) -> str:
        """Returns the hex version of this cell with to_hex()."""
        return self.to_hex()

    def __repr__(self) -> str:
        """Returns debug information for this cell, including most of it's
        parameters."""
        s = 'Cell {\n'
        s += f'\thex = {self.to_hex()}\n'
        s += f'\tx = {self.x}\n'
        s += f'\ty = {self.y}\n'
        s += f'\tnorth = {self.north}\n'
        s += f'\teast = {self.east}\n'
        s += f'\tsouth = {self.south}\n'
        s += f'\twest = {self.west}\n'
        s += '}'
        return s

    def __hash__(self) -> int:
        """Returns a hash for the cell."""
        return hash((self.x, self.y))
