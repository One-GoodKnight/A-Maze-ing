try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from maze import *
from maze_generator import *
from display import *
from helpers import *
from game import *
from constants import *
import random
import time

def display(params):
    start = time.time()
    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player = params
    mlx_maze_display.display_maze(maze, 0, 0)
    display_player(image, player)
    rotate_image(image, game.angle)
    # makes the loop take twice as much time third of the time -> freezes
    mlx.mlx_clear_window(mlx_ptr, win_ptr)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)
    end = time.time()
    print(end-start)

def game_loop(params):
    start = time.time()

    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player = params

    #print(game.delta_time)
    game.rotate()
    game.gravity(maze.maze, maze.cell_size, player)

    display((mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player))

    game.deltatime = time.time() - start

# TODO generate new maze, change colors, etc
def handle_key_press(keycode, params):
    mlx, mlx_ptr, game = params
    if keycode == 0xFF1B or keycode == 0x71:
        params[0].mlx_loop_exit(params[1])

    if keycode == 0xff51:
        game.left_rotate = True
    if keycode == 0xff53:
        game.right_rotate = True

def handle_key_release(keycode, params):
    mlx, mlx_ptr, game = params

    if keycode == 0xff51:
        game.left_rotate = False
    if keycode == 0xff53:
        game.right_rotate = False

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
        random.seed(config['seed'] if 'seed' in config else 42)
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
        print(f"An error occured during file parsing: {e}")
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
    window_width, window_height, maze.cell_size = CalculateSize.calculate(screen_width, screen_height, maze.width, maze.height)
    win_ptr = mlx.mlx_new_window(mlx_ptr, window_width, window_height, "A-maze-ing")

    image = Image(mlx, mlx_ptr, window_width, window_height)
    mlx_maze_display = MazeDisplay(mlx, image)

    game = Game(maze.width, maze.height)
    player_size = int(maze.cell_size * PLAYER_SIZE)
    player = Player(maze.entry[0], maze.entry[1], player_size, image.width, image.height, maze.cell_size)

    mlx.mlx_do_key_autorepeatoff(mlx_ptr)

    client_message_event = 33
    mlx.mlx_hook(win_ptr, client_message_event, 0, handle_close, (mlx, mlx_ptr))

    key_press_event, key_press_mask = (2, 1)
    key_release_event, key_release_mask = (3, 2)
    mlx.mlx_hook(win_ptr, key_press_event, key_press_mask, handle_key_press, (mlx, mlx_ptr, game))
    mlx.mlx_hook(win_ptr, key_release_event, key_release_mask, handle_key_release, (mlx, mlx_ptr, game))

    #mlx.mlx_string_put(mlx_ptr, win_ptr, int(screen_width / 2), int(screen_height / 2) - 5, 0x00FFFFFF, "Hello world")

    game.time = time.time()

    mlx.mlx_loop_hook(mlx_ptr, game_loop, (mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player))

    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_do_key_autorepeaton(mlx_ptr)
    mlx.mlx_destroy_image(mlx_ptr, image.ptr)
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)

if __name__ == "__main__":
    main()
