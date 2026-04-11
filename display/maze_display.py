try:
    from mlx import Mlx
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from constants import MAZE_BORDER_WIDTH_PERCENT, MAZE_BORDER_COLOR
from constants import MAZE_BACKGROUND_COLOR, GREEN, RED
from maze import Maze
from maze_generator import Cell
from .image import Image
#import cProfile

class MazeDisplay():
    def __init__(self, mlx: Mlx, image: Image) -> None:
        self.mlx = mlx
        self.width = image.width
        self.height = image.height

        self.image = image
        self.data = image.data
        self.fmt = image.fmt

    def write_cell(self, cell: Cell,
                   cell_width: int, cell_height: int, x: int, y: int) -> None:
        vline_width: int = int(cell_width / 100 * MAZE_BORDER_WIDTH_PERCENT / 2)
        hline_width: int = int(cell_height / 100 * MAZE_BORDER_WIDTH_PERCENT / 2)
        xpos: int = cell_width * x
        ypos: int = cell_height * y
        if (cell.color != 0):
            self.image.draw_rect(
                (xpos + vline_width, ypos + hline_width),
                (xpos + cell_width - vline_width, ypos + cell_height - hline_width),
                cell.color
            )
        if cell.north:
            self.image.draw_rect(
                (xpos              - vline_width, ypos - hline_width),
                (xpos + cell_width + vline_width, ypos + hline_width),
                MAZE_BORDER_COLOR
            )
        if cell.east:
            self.image.draw_rect(
                (xpos + cell_width - vline_width, ypos               - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                MAZE_BORDER_COLOR
            )
        if cell.south:
            self.image.draw_rect(
                (xpos              - vline_width, ypos + cell_height - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                MAZE_BORDER_COLOR
            )
        if cell.west:
            self.image.draw_rect(
                (xpos - vline_width, ypos               - hline_width),
                (xpos + vline_width, ypos + cell_height + hline_width),
                MAZE_BORDER_COLOR
            )

    def maze_to_image(self, maze: Maze) -> None:
        self.image.set_to(MAZE_BACKGROUND_COLOR)
        cell_width = int(self.width / maze.width)
        cell_height = int(self.height / maze.height)
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                self.write_cell(cell, cell_width, cell_height, x, y)

        start = Cell(x=maze.entry[0], y=maze.entry[1], color=GREEN)
        end = Cell(x=maze.exit[0], y=maze.exit[1], color=RED)
        self.write_cell(start, cell_width, cell_height, start.x, start.y)
        self.write_cell(end, cell_width, cell_height, end.x, end.y)

    def display_maze(self, maze: Maze, x: int, y: int) -> None:
        #cProfile.runctx('self.maze_to_image(maze)', globals(), locals())
        if not maze:
            return
        self.maze_to_image(maze)
