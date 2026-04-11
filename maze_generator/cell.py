from pydantic import BaseModel, Field
from typing import Self
from .directions import Direction

class Cell(BaseModel):
    x: int          = Field(ge=0)
    y: int          = Field(ge=0)
    north: bool     = Field(default=False)
    east: bool      = Field(default=False)
    south: bool     = Field(default=False)
    west: bool      = Field(default=False)
    dir_north: bool = Field(default=False)
    dir_east: bool  = Field(default=False)
    dir_south: bool = Field(default=False)
    dir_west: bool  = Field(default=False)
    color: int      = Field(default=0)

    @staticmethod
    def from_hex(hex: str, x: int, y: int) -> Self:
        nb = int(hex, 16)
        north = nb & 1
        east = nb >> 1 & 1
        south = nb >> 2 & 1
        west = nb >> 3 & 1
        return Cell(x=x, y=y, north=north, east=east, south=south, west=west)

    def to_int(self) -> int:
        north = int(self.north)
        east = int(self.east) << 1
        south = int(self.south) << 2
        west = int(self.west) << 3
        return north + east + south + west

    def to_hex(self) -> str:
        return f"{self.to_int():X}"

    def isolated(self) -> bool:
        return (
            self.north and
            self.east and
            self.south and
            self.west
        )

    @staticmethod
    def manhattan_distance(c1: Self, c2: Self) -> int:
        return abs(c1.x - c2.x) + abs(c1.y - c2.y)

    def __eq__(self, cell: Self) -> bool:
        return (self.x == cell.x and self.y == cell.y)

    def __str__(self) -> str:
       return self.to_hex()

    def __repr__(self) -> str:
        return self.to_hex()

    def __hash__(self):
        return hash((self.x, self.y))

