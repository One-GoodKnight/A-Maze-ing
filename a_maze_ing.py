try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from maze import *
from maze_generator import *
from display import *
from helpers import *
import random

def display_maze(params):
    params[0].display(params[1], 0, 0)

def handle_key_hook(keycode, params) -> None:
    if keycode == 0xFF1B or keycode == 0x71:
        params[0].mlx_loop_exit(params[1])
    # TODO generate new maze, change colors, etc

def handle_close(params):
    params[0].mlx_loop_exit(params[1])

def main() -> None:
    import sys

    argc = len(sys.argv)
    if argc != 2:
        print("The program should be run with: python3 a_maze_ing.py filename")
        return 1

    config = {}
    filename = sys.argv[1]
    try:
        config = parse_config_file(filename)
        filename = "logo.42"
        parse_logo_data = parse_logo(filename, config['width'], config['height'])
        logo, logo_width, logo_height = parse_logo_data if parse_logo_data else (None, None, None)
    except FileNotFoundError as _:
        print(f"Could not find the file '{filename}'")
        return 1
    except PermissionError as _:
        print(f"Cannot read config file '{filename}', permission denied")
        return 1
    except Exception as e:
        print(f"An error occured during the file parsing: {e}")
        return 1

    if (not logo or (len(logo) >= 1 and ((logo_width + 2 > config['width']) or (logo_height + 2 > config['height'])))):
        sys.stderr.write("Error, logo too small, starting the maze without it.\n")
        logo = []

    temp_entry = Cell(x=config['entry'][0], y=config['entry'][1])
    temp_exit = Cell(x=config['exit'][0], y=config['exit'][1])
    if (temp_entry in logo):
        sys.stderr.write("Error: entry on logo, starting the maze without logo.\n")
        logo = []
    elif (temp_exit in logo):
        sys.stderr.write("Error: exit on logo, starting the maze without logo.\n")
        logo = []

    random.seed(10)
    maze_generator = MazeGenerator(**config)
    maze_generated = maze_generator.build_maze(logo)
    try:
        maze_generator.build_output(maze_generated)
    except PermissionError as _:
        print(f"Cannot write to output '{maze.output_file}', permission denied")
        return 1

    maze = Maze(
        maze=maze_generated,
        solution="",
        width=maze_generator.width,
        height=maze_generator.height,
        entry=maze_generator.entry,
        exit=maze_generator.exit,
        output_file=maze_generator.output_file,
        perfect=maze_generator.perfect
    )

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    _, screen_width, screen_height = mlx.mlx_get_screen_size(mlx_ptr)
    window_width, window_height = CalculateWindowSize.calculate(screen_width, screen_height, maze.width, maze.height)
    win_ptr = mlx.mlx_new_window(mlx_ptr, window_width, window_height, "A-maze-ing")

    mlx.mlx_key_hook(win_ptr, handle_key_hook, (mlx, mlx_ptr))
    client_message_event = 33
    mlx.mlx_hook(win_ptr, client_message_event, 0, handle_close, (mlx, mlx_ptr))

    #mlx.mlx_string_put(mlx_ptr, win_ptr, int(screen_width / 2), int(screen_height / 2) - 5, 0x00FFFFFF, "Hello world")

    mlx_maze_display = MlxMazeDisplay(mlx, mlx_ptr, win_ptr, window_width, window_height)
    mlx.mlx_loop_hook(mlx_ptr, display_maze, (mlx_maze_display, maze))

    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)

if __name__ == "__main__":
    main()
