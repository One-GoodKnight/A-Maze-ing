from .image import Image
from .color import endian_color
from game import Player
import numpy as np

def display_player(image: Image, player: Player):
    x0, y0 = (0, 0)
    x1, y1 = (100, 100)
    color = endian_color(image, player.color)
    rect = np.tile(color, (y1 - y0, x1 - x0))
    image.data[y0 : y1, x0*image.bytes_pp : x1*image.bytes_pp] = rect
