try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from typing import Callable
from ctypes import c_void_p, c_ubyte
from maze import Maze
from maze_generator import Cell
from .image import Image
import numpy as np
import time
import cProfile
try:
    import cv2
except ImportError as e:
    raise SystemExit(f"Unable to import cv2: {e}")

class MlxMazeDisplay():
    def __init__(self, mlx: Mlx, image: Image) -> None:
        self.mlx = mlx
        self.width = image.width
        self.height = image.height

        self.image = image
        self.data = image.data
        self.bpp = image.bpp
        self.fmt = image.fmt

    def draw_rect(self, start: tuple[int, int], end: tuple[int, int],
                  argb: int) -> None:
        x0, y0 = (min(self.width - 1, max(0, start[0])), min(self.height - 1, max(0, start[1])))
        x1, y1 = (min(self.width - 1, max(0, end[0])), min(self.height - 1, max(0, end[1])))

        bytes_pp = self.bpp // 8

        if (not argb in self.image.colors):
            if self.fmt == 1:
                self.image.colors[argb] = np.array([
                    argb >> 24 & 0xFF, argb >> 16 & 0xFF,
                    argb >> 8 & 0xFF, argb & 0xFF],
                dtype=np.uint8)
            else:
                self.image.colors[argb] = np.array([
                    argb & 0xFF, argb >> 8 & 0xFF,
                    argb >> 16 & 0xFF, argb >> 24 & 0xFF],
                dtype=np.uint8)

        rect = np.tile(self.image.colors[argb], (y1 - y0, x1 - x0))
        self.data[y0 : y1, x0*bytes_pp : x1*bytes_pp] = rect

    def write_cell(self, cell: Cell,
                   cell_width: int, cell_height: int, x: int, y: int) -> None:
        WALL_COLOR: int = 0xFF_A4_34_EB
        LINE_WIDTH_PERCENT: int = 20

        vline_width: int = int(cell_width / 100 * LINE_WIDTH_PERCENT / 2)
        hline_width: int = int(cell_height / 100 * LINE_WIDTH_PERCENT / 2)
        xpos: int = cell_width * x
        ypos: int = cell_height * y
        if (cell.color != 0):
            self.draw_rect((xpos, ypos), (xpos+cell_width, ypos+cell_height), cell.color)
        if cell.north:
            self.draw_rect(
                (xpos              - vline_width, ypos - hline_width),
                (xpos + cell_width + vline_width, ypos + hline_width),
                WALL_COLOR
            )
        if cell.east:
            self.draw_rect(
                (xpos + cell_width - vline_width, ypos               - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR
            )
        if cell.south:
            self.draw_rect(
                (xpos              - vline_width, ypos + cell_height - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR
            )
        if cell.west:
            self.draw_rect(
                (xpos - vline_width, ypos               - hline_width),
                (xpos + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR
            )

    def set_to(self, color: int) -> None:
        self.draw_rect(
            (0, 0),
            (self.width, self.height),
            color
        )

    def maze_to_image(self, maze: Maze) -> None:
        self.set_to(0xFF_FF_FF_FF)
        cell_width = int(self.width / maze.width)
        cell_height = int(self.height / maze.height)
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                self.write_cell(cell, cell_width, cell_height, x, y)

    def rotate_image(self) -> None:
        img = self.data.reshape(self.height, self.width, self.bpp // 8)
        center = (self.width // 2, self.height // 2)
        matrix = cv2.getRotationMatrix2D(center, -45, scale=(1 / 1.414))
        rotated = cv2.warpAffine(img, matrix, (self.width, self.height))
        self.data[:self.height, :self.width * (self.bpp // 8)] = rotated.reshape(self.height, self.width * (self.bpp // 8))

    def display(self, maze: Maze, x: int, y: int) -> None:
        #cProfile.runctx('self.maze_to_image(maze)', globals(), locals())
        self.maze_to_image(maze)
        self.rotate_image()
