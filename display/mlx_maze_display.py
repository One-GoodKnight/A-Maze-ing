try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from typing import Callable
from ctypes import c_void_p, c_ubyte
from maze import Maze
from maze_generator import Cell
from numpy import ndarray

class MlxMazeDisplay():
    def __init__(self, mlx: Mlx, mlx_ptr: c_void_p, win_ptr: c_void_p,
                 width: int, height: int) -> None:
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.width = width
        self.height = height

    @staticmethod
    def get_set_pixel(data: c_ubyte, bits_per_pixel: int,
                        line_size: int, format: int) -> Callable:
        def set_pixel(argb: int, x: int, y: int):
            offset = x * (bits_per_pixel // 8) + y * line_size
            if format == 0:
                data[offset:offset+4] = bytes(argb.to_bytes(4, 'little'))
            else:
                data[offset:offset+4] = bytes(argb.to_bytes(4, 'big'))
        return set_pixel

    def draw_rect(self, start: tuple[int, int], end: tuple[int, int],
                  argb: int, set_pixel: Callable) -> None:
        for y in range(start[1], end[1]):
            for x in range(start[0], end[0]):
                if x >= 0 and x < self.width and y >= 0 and y < self.height:
                    set_pixel(argb, x, y)

    def write_cell(self, cell: Cell, set_pixel: Callable,
                   cell_width: int, cell_height: int, x: int, y: int) -> None:
        WALL_COLOR: int = 0xFF_A4_34_EB
        LINE_WIDTH_PERCENT: int = 20
        vline_width: int = int(cell_width / 100 * LINE_WIDTH_PERCENT / 2)
        hline_width: int = int(cell_height / 100 * LINE_WIDTH_PERCENT / 2)
        xpos: int = cell_width * x
        ypos: int = cell_height * y
        if (cell.color != 0):
            self.draw_rect((xpos, ypos), (xpos+cell_width, ypos+cell_height), cell.color, set_pixel)
        if cell.north:
            self.draw_rect(
                (xpos              - vline_width, ypos - hline_width),
                (xpos + cell_width + vline_width, ypos + hline_width),
                WALL_COLOR,
                set_pixel
            )
        if cell.east:
            self.draw_rect(
                (xpos + cell_width - vline_width, ypos               - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR,
                set_pixel
            )
        if cell.south:
            self.draw_rect(
                (xpos              - vline_width, ypos + cell_height - hline_width),
                (xpos + cell_width + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR,
                set_pixel
            )
        if cell.west:
            self.draw_rect(
                (xpos - vline_width, ypos               - hline_width),
                (xpos + vline_width, ypos + cell_height + hline_width),
                WALL_COLOR,
                set_pixel
            )

    def set_to(self, color: int, set_pixel: Callable) -> None:
        self.draw_rect(
            (0, 0),
            (self.width, self.height),
            color,
            set_pixel
        )

    def maze_to_image(self, maze: Maze) -> c_void_p:
        img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.width, self.height)
        data, bpp, line_size, fmt = self.mlx.mlx_get_data_addr(img_ptr)
        set_pixel = self.get_set_pixel(data, bpp, line_size, fmt)
        print("super long")
        self.set_to(0xFF_FF_FF_FF, set_pixel)
        print("1")
        cell_width = int(self.width / maze.width)
        cell_height = int(self.height / maze.height)
        print("un peu long")
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                self.write_cell(cell, set_pixel, cell_width, cell_height, x, y)
        return img_ptr

    def display(self, maze: Maze, x: int, y: int) -> None:
        img_ptr = self.maze_to_image(maze)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img_ptr, x, y)
        self.mlx.mlx_destroy_image(self.mlx_ptr, img_ptr)
