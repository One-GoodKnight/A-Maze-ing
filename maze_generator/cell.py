from pydantic import BaseModel, Field
from typing import Self
from enum import StrEnum

class Direction(StrEnum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'

class Cell(BaseModel):
    x: int      = Field(ge=0)
    y: int      = Field(ge=0)
    north: bool = Field(default=False)
    east: bool  = Field(default=False)
    south: bool = Field(default=False)
    west: bool  = Field(default=False)

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

