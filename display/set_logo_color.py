from .image import Image
from maze_generator import Cell
from constants import LOGO_COLOR


def set_logo_color(image: Image, logo: list[Cell]) -> None:
    for cell in logo:
        cell.color = image.endian_color_int(LOGO_COLOR)
