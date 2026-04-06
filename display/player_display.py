from .image import Image
from .color import endian_color
from constants import *
from game import Player
import numpy as np

def display_player(image: Image, player: Player):
    hline_width: int = int(player.size / 100 * MAZE_BORDER_WIDTH_PERCENT / 2)
    vline_width: int = int(player.size / 100 * MAZE_BORDER_WIDTH_PERCENT / 2)

    player_width = player.size - (2 * hline_width)
    player_height = player.size - (2 * hline_width)

    x0, y0 = (int(player.x + vline_width), int(player.y + hline_width))
    x1, y1 = (int(player.x + player_width + vline_width), int(player.y + player_height + hline_width))

    color = endian_color(image, player.color)

    rect = np.tile(color, (y1 - y0, x1 - x0))
    image.data[y0 : y1, x0*image.bytes_pp : x1*image.bytes_pp] = rect
