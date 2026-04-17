from .image import Image
from constants import Const
from game import Player
import numpy as np


def display_border(image: Image, player: Player, hline_width: int,
                   vline_width: int, player_width: int,
                   player_height: int) -> None:
    """Draw the player's border on the given Image."""
    x0 = int(player.x + vline_width)
    y0 = int(player.y + hline_width)
    x1 = int(player.x + player_width + vline_width)
    y1 = int(player.y + player_height + hline_width)
    color = image.endian_color(Const.PLAYER_BORDER_COLOR)
    assert color is not None
    rect = np.tile(color, (y1 - y0, x1 - x0))
    image.data[y0: y1, x0*image.bytes_pp: x1*image.bytes_pp] = rect


def display_player(image: Image, player: Player) -> None:
    """Draw the player on the given Image."""
    b_width_perc = Const.MAZE_BORDER_WIDTH_PERCENT
    hline_width: int = int(player.size / 100 * b_width_perc / 2)
    vline_width: int = int(player.size / 100 * b_width_perc / 2)
    player_width = player.size - (2 * vline_width)
    player_height = player.size - (2 * hline_width)
    display_border(image, player, hline_width, vline_width,
                   player_width, player_height)
    border_thickness = Const.PLAYER_BORDER * player.size
    x0 = int(player.x + vline_width + border_thickness)
    y0 = int(player.y + hline_width + border_thickness)
    x1 = int(player.x + player_width + vline_width - border_thickness)
    y1 = int(player.y + player_height + hline_width - border_thickness)
    color = image.endian_color(Const.PLAYER_COLOR)
    assert color is not None
    rect = np.tile(color, (y1 - y0, x1 - x0))
    image.data[y0: y1, x0*image.bytes_pp: x1*image.bytes_pp] = rect
