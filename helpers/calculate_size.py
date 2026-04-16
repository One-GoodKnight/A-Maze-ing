from constants import DEFAULT_CELL_SIZE, WINDOW_MARGIN


class CalculateSize():
    """
    Provides a method to calculate the right size for the window.
    """
    @staticmethod
    def calculate(screen_width: int, screen_height: int,
                  cells_x: int, cells_y: int) -> tuple[int, int, int]:
        """
        Calculates the right window size and cell size for the monitor and
        the maze that will generate.
        
        Attributes:
            screen_width (int): Width of the monitor in pixels.
            screen_height (int): Height of the monitor in pixels.
            cells_x (int): Width of the maze.
            cells_y (int): Height of the maze.

        Returns:
            tuple[int, int, int]: Tuple with window width, window height and
                and cell_size that will be used for the rest of the program.
        """
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
