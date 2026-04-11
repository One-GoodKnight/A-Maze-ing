from constants import DEFAULT_CELL_SIZE, WINDOW_MARGIN
from typing import Tuple

class CalculateSize():
    @staticmethod
    def calculate(screen_width: int, screen_height: int, cells_x: int, cells_y: int)-> Tuple[int, int, int]:
        cell_size = DEFAULT_CELL_SIZE

        window_width = cells_x * cell_size
        window_height = cells_y * cell_size

        screen_width -= WINDOW_MARGIN
        screen_height -= WINDOW_MARGIN

        while (cell_size > 1 and window_width > screen_width):
            cell_size -= 1
            window_width = cells_x * cell_size
            window_height = cells_y * cell_size

        while (cell_size > 1 and window_height > screen_height):
            cell_size -= 1
            window_width = cells_x * cell_size
            window_height = cells_y * cell_size

        return (window_width, window_height, cell_size)
