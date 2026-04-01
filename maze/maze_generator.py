from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Self, ClassVar

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

    def build_output(self):
        with open(self.output_file, 'w') as f:
            f.write("a")


