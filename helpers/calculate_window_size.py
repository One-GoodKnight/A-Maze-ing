from typing import Tuple

class CalculateWindowSize():
    DEFAULT_CELL_SIZE: int = 75
    WINDOW_MARGIN: int = 200

    @staticmethod
    def calculate(screen_width: int, screen_height: int, cells_x: int, cells_y: int)-> Tuple[int, int]:
        cell_size = CalculateWindowSize.DEFAULT_CELL_SIZE
        w_marg = CalculateWindowSize.WINDOW_MARGIN

        window_width = cells_x * cell_size
        window_height = cells_y * cell_size

        screen_width -= w_marg
        screen_height -= w_marg

        while (cell_size > 1 and window_width > screen_width):
            cell_size -= 1
            window_width = cells_x * cell_size
            window_height = cells_y * cell_size

        while (cell_size > 1 and window_height > screen_height):
            cell_size -= 1
            window_width = cells_x * cell_size
            window_height = cells_y * cell_size

        return (window_width, window_height)
