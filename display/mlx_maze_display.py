try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from typing import Callable
from ctypes import c_void_p, c_ubyte
from maze import Maze
from maze_generator import Cell
import numpy as np
import time
import cProfile

class MlxMazeDisplay():
    def __init__(self, mlx: Mlx, mlx_ptr: c_void_p, win_ptr: c_void_p,
                 width: int, height: int, img_ptr: c_void_p) -> None:
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.width = width
        self.height = height

        self.img_ptr = img_ptr
        data, bpp, line_size, fmt = self.mlx.mlx_get_data_addr(img_ptr)
        self.data = np.ctypeslib.as_array(data, np.uint8)
        self.data = self.data.reshape(height, line_size)
        self.bpp = bpp
        self.line_size = line_size
        self.fmt = fmt

        self.colors = {}

    def draw_rect(self, start: tuple[int, int], end: tuple[int, int],
                  argb: int) -> None:
        x0, y0 = (min(self.width - 1, max(0, start[0])), min(self.height - 1, max(0, start[1])))
        x1, y1 = (min(self.width - 1, max(0, end[0])), min(self.height - 1, max(0, end[1])))

        bytes_pp = self.bpp // 8

        if (not argb in self.colors):
            if self.fmt == 1:
                self.colors[argb] = np.array([
                    argb >> 24 & 0xFF, argb >> 16 & 0xFF,
                    argb >> 8 & 0xFF, argb & 0xFF],
                dtype=np.uint8)
            else:
                self.colors[argb] = np.array([
                    argb & 0xFF, argb >> 8 & 0xFF,
                    argb >> 16 & 0xFF, argb >> 24 & 0xFF],
                dtype=np.uint8)

        rect = np.tile(self.colors[argb], (y1 - y0, x1 - x0))
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

    def maze_to_image(self, maze: Maze) -> c_void_p:
        self.set_to(0xFF_FF_FF_FF)
        cell_width = int(self.width / maze.width)
        cell_height = int(self.height / maze.height)
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                self.write_cell(cell, cell_width, cell_height, x, y)
        return self.img_ptr

    def display(self, maze: Maze, x: int, y: int) -> None:
        self.npdata = np.zeros(len(self.data), dtype=np.uint8)
        #cProfile.runctx('self.maze_to_image(maze)', globals(), locals())
        img_ptr = self.maze_to_image(maze)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img_ptr, x, y)
