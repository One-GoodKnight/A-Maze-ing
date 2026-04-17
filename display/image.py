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
from typing import Any, Optional
from ctypes import c_void_p


class Image():
    """
    Manages Mlx images used to write to the window.
    Stores variables used to operate on the image.
    """
    def __init__(self, mlx: Mlx, mlx_ptr: c_void_p, width: int, height: int,
                 font: Optional[Font] = None) -> None:
        """
        Create and store a new Mlx image, as well as
        all the variables used to operate on that image.

        Attributes:
            mlx (Mlx): Mlx instance.
            mlx_ptr (c_void_p): Pointer to the mlx window.
            width (int): Width of the image.
            height (int): Height of the image.
            font (Font): Optional variable containing an
                         instance of the Font class.
        """
        self.width = width
        self.height = height
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        data, bpp, self.line_size, self.fmt = mlx.mlx_get_data_addr(self.ptr)
        self.data = np.ctypeslib.as_array(data)
        self.data = self.data.reshape(height, self.line_size)
        self.bits_pp = bpp
        self.bytes_pp = bpp // 8
        self.font = font

    @lru_cache
    def endian_color(self, argb: int | None) -> Optional[NDArray[np.uint8]]:
        """
        Convert an ARGB integer representation in
        a numpy array containing 4 uint8 values,
        formated according to the image format.

        Args:
            argb (int | None): Integer representation of an ARGB color.

        Returns:
            NumpyArray[4 * uint8]: a numpy array containing 4 uint8 values,
            formated according to the image format
            if a color is given to the function. None otherwise.
        """
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
        """
        Fill the image's pixels between start and end with the argb color.

        Args:
            start (tuple(x: int, y: int)): Top left coordinate of
                the rectangle to be drawn.
            end (tuple(x: int, y: int)): Bottom right coordinate of
                the rectangle to be drawn.
            argb (int): Integer representation of an ARGB color.

        Returns:
            None
        """
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
        """Set all the pixels of the image to the specified color."""
        self.draw_rect(
            (0, 0),
            (self.width, self.height),
            color
        )

    def rotate(self, angle: float) -> None:
        """Rotate the image from the specified angle."""
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
        """Set the font variable allowing to draw text on the image."""
        self.font = font

    def print_char(self, x: int, y: int, char: str, **kwargs: Any) -> None:
        """
        Draw a single character if it is available in self.font.

        Args:
            x (int): X coordinate from which to draw the character.
            y (int): Y coordinate from which to draw the character.
            char (str): A single character to be drawn.
                It needs to be available in the Font given to Image.

        Key word arguments:
            color (int): ARGB representation of the color to draw
                the character with. Default to BLACK if omited.
            size (int): Number of times the function should draw each pixel
                of the character to increase its size.

        Returns:
            None
        """
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
        """
        Draw a string of character on the image.
        Only draw character available in the Font given to Image,
        display a space otherwise.

        Args:
            x (int): X coordinate from which to draw string.
            y (int): Y coordinate from which to draw string.
            string (str): String of character to be drawn to the image.

        Keyword arguments:
            color (int): ARGB representation of the color to draw
                the characters with. Default to BLACK.
            bg_color (int): ARGB representation of the color to draw
                the background of the characters with. Default to None.
            size (int): Number of times the function should draw each pixel
                of the characters to increase their size. Default to 1.
            center (bool): If True, the x and y coordinate will
                be relative to the center of the image. Default to False.

        Returns:
            None
        """
        if self.font is None:
            return
        font = self.font
        bg_color = kwargs.get('bg_color', None)
        size = max(kwargs.get('size', 1), 1)
        center = kwargs.get('center', False)
        char_width, char_height = (font.width * size, font.height * size)
        lines = string.splitlines()
        y = y if not center else (
            (self.height // 2 + y) - ((char_height * len(lines)) // 2)
        )
        x = x if not center else (self.width // 2 + x)
        for i, line in enumerate(lines):
            bg_width = len(line) * char_width
            curr_x = x if not center else (x - bg_width // 2)
            curr_y = y + char_height * i
            if bg_color is not None:
                self.draw_rect(
                    (curr_x, curr_y),
                    (curr_x + bg_width, curr_y + char_height),
                    bg_color
                )
            offset = 0
            for char in line:
                self.print_char(curr_x + offset, curr_y, char, **kwargs)
                offset += char_width
