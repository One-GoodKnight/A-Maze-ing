try:
    from mlx import Mlx  # type: ignore[import-untyped]
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
from typing import Any
from ctypes import c_void_p


class Image():
    def __init__(self, mlx: Mlx, mlx_ptr: c_void_p, width: int, height: int,
                 font: Font | None = None) -> None:
        self.width = width
        self.height = height
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        data, bpp, self.line_size, self.fmt = mlx.mlx_get_data_addr(self.ptr)
        self.data = np.ctypeslib.as_array(
            data, np.uint8
        )  # type: ignore[call-overload]
        self.data = self.data.reshape(height, self.line_size)
        self.bits_pp = bpp
        self.bytes_pp = bpp // 8
        self.font: Font | None = font

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
        color = self.endian_color(argb)
        assert color is not None
        self.data[
            y0: y1,
            x0 * self.bytes_pp: x1 * self.bytes_pp
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

    def print_char(self, x: int, y: int, char: str, **kwargs: Any) -> None:
        if self.font is None:
            return
        font = self.font
        color = kwargs.get('color', BLACK)
        size = max(kwargs.get('size', 1), 1)
        char_dict = font.chars.get(char)
        if char_dict is None:
            return
        for i in range(font.width):
            for j in range(font.height):
                if char_dict[j][i] == '#' and color is not None:
                    start = (x + i * size, y + j * size)
                    end = (start[0] + size, start[1] + size)
                    self.draw_rect(start, end, color)

    def print(self, x: int, y: int, string: str, **kwargs: Any) -> None:
        if self.font is None:
            return
        font = self.font
        bg_color = kwargs.get('bg_color', None)
        size = max(kwargs.get('size', 1), 1)
        char_width, char_height = (font.width * size, font.height * size)
        bg_width = len(string) * char_width
        x = x if x >= 0 else (self.width // 2) - (bg_width // 2)
        y = y if y >= 0 else (self.height // 2) - (char_height // 2)
        if bg_color is not None:
            self.draw_rect((x, y), (x + bg_width, y + char_height), bg_color)
        offset = 0
        for char in string:
            self.print_char(x + offset, y, char, **kwargs)
            offset += char_width
