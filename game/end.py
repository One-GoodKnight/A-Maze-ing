from .game import Player


def check_end(player: Player, cell_size: int, exit: tuple[int, int]) -> bool:
    x, y = (player.center_x // cell_size, player.center_y // cell_size)

    if (x == exit[0] and y == exit[1]):
        return True

    return False
