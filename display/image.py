try:
    from mlx import Mlx
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
try:
    import cv2
except ImportError as e:
    raise SystemExit(f"Unable to import cv2: {e}")
import numpy as np
from numpy.typing import NDArray
from constants import MAZE_SCALE, BLACK
from .font import Font
from functools import lru_cache


class Image():
    def __init__(self, mlx: Mlx, mlx_ptr, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        data, bpp, self.line_size, self.fmt = mlx.mlx_get_data_addr(self.ptr)
        self.data = np.ctypeslib.as_array(data, np.uint8)
        self.data = self.data.reshape(height, self.line_size)
        self.bits_pp = bpp
        self.bytes_pp = bpp // 8
        self.font: Font | None = None

    @lru_cache
    def endian_color(self, argb: int | None) -> NDArray[np.uint8] | None:
        if argb is None:
            return None
        if self.fmt == 1:
            color = np.array([
                    argb >> 24 & 0xFF, argb >> 16 & 0xFF,
                    argb >> 8 & 0xFF, argb & 0xFF
                ], dtype=np.uint8
            )
        else:
            color = np.array([
                    argb & 0xFF, argb >> 8 & 0xFF,
                    argb >> 16 & 0xFF, argb >> 24 & 0xFF
                ], dtype=np.uint8
            )
        return color

    def draw_rect(self, start: tuple[int, int], end: tuple[int, int],
                  argb: int) -> None:
        x0 = min(self.width - 1, max(0, start[0]))
        y0 = min(self.height - 1, max(0, start[1]))
        x1 = min(self.width - 1, max(0, end[0]))
        y1 = min(self.height - 1, max(0, end[1]))
        bytes_pp = self.bytes_pp
        color = self.endian_color(argb)
        self.data[
            y0: y1,
            x0*bytes_pp: x1*bytes_pp
        ] = np.tile(color, x1 - x0)

    def set_to(self, color: int) -> None:
        self.draw_rect(
            (0, 0),
            (self.width, self.height),
            color
        )

    def rotate(self, angle: float) -> None:
        img = self.data.reshape(self.height, self.width, self.bytes_pp)
        center = (self.width // 2, self.height // 2)
        matrix = cv2.getRotationMatrix2D(
            center, -angle, scale=(1 / 1.414) * MAZE_SCALE
        )
        color = (0, 0, 0, 255) if self.fmt == 0 else (255, 0, 0, 0)
        rotated = cv2.warpAffine(
            img, matrix, (self.width, self.height),
            borderMode=cv2.BORDER_CONSTANT, borderValue=color
        )
        self.data[
            :self.height,
            :self.width * (self.bytes_pp)
        ] = rotated.reshape(self.height, self.width * (self.bytes_pp))

    def set_font(self, font: Font) -> None:
        self.font = font

    def print_char(self, x: int, y: int,
                   char: str, **kwargs) -> None:
        font = self.font
        color = self.endian_color(kwargs.get('color', BLACK))
        bg_color = self.endian_color(kwargs.get('bg_color', None))
        size = kwargs.get('size', 1)
        if size <= 0:
            size = 1
        letter = font.letters.get(char)
        if letter is None:
            return
        for i in range(font.width * size):
            for j in range(font.height * size):
                x_coord = (x + i) * self.bytes_pp
                y_coord = y + j
                if (y_coord >= 0 and y_coord < self.height and x_coord >= 0
                        and x_coord < self.width * self.bytes_pp):
                    if letter[j // size][i // size] == '#':
                        if color is not None:
                            self.data[
                                y_coord,
                                x_coord: x_coord + self.bytes_pp
                            ] = color
                    else:
                        if bg_color is not None:
                            self.data[
                                y_coord,
                                x_coord: x_coord + self.bytes_pp
                            ] = bg_color

    def print(self, x: int, y: int, text: str, **kwargs) -> None:
        if not text.isascii():
            raise ValueError(f"Invalid text: '{text}' "
                             "contains non ASCII characters")
        font = self.font
        color = kwargs.get('color', BLACK)
        bg_color = kwargs.get('bg_color', None)
        size = kwargs.get('size', 1)
        if size <= 0:
            size = 1
        if x == -1:
            x = (self.width // 2) - (len(text) * font.width * size // 2)
        if y == -1:
            y = (self.height // 2) - (font.height * size // 2)
        for i, char in enumerate(text):
            offset = i * font.width * size
            if char == ' ' and bg_color is not None:
                self.draw_rect(
                    (x + offset, y),
                    (x + offset + (font.width * size), y + font.height * size),
                    bg_color
                )
            else:
                self.print_char(x + offset, y, char, color=color,
                                bg_color=bg_color, size=size)
