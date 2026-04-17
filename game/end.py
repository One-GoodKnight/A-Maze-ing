from .player import Player


def check_end(player: Player, cell_size: int, exit: tuple[int, int]) -> bool:
    """
    Checks if the game should end based on player and end pos.

    Attributes:
        player (Player): Player instance for the game.
        cell_size (int): Size of the cells in pixel.
        exit (tuple[int, int]): Exit cell of the maze.

    Returns:
        bool: True if player on end cell else False.
    """
    x, y = (player.center_x // cell_size, player.center_y // cell_size)
    if (x == exit[0] and y == exit[1]):
        return True
    return False
