from maze import *
try:
    from mlx import *
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")


def handle_key_hook(keycode, params) -> None:
    if keycode == 0xFF1B or keycode == 0x71:
        params[0].mlx_loop_exit(params[1])
    # print(keycode)
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
    try:
        config = parse_config_file(sys.argv[1])
    except FileNotFoundError as _:
        print(f"Could not find the file {sys.argv[1]}")
        return 1
    except PermissionError as e:
        print(f"Cannot read config file '{sys.argv[1]}', permission denied")
        return 1
    except Exception as e:
        print(f"An error occured during the file parsing: {e}")
        return 1

    maze = MazeGenerator(**config)
    print(maze)

    try:
        maze.build_output()
    except PermissionError as e:
        print(f"Cannot write to output '{maze.output_file}', permission denied")
        return 1
    
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    _, screen_width, screen_height = mlx.mlx_get_screen_size(mlx_ptr)
    win_ptr = mlx.mlx_new_window(mlx_ptr, screen_width, screen_height, "A-maze-ing")

    mlx.mlx_key_hook(win_ptr, handle_key_hook, (mlx, mlx_ptr))
    mlx.mlx_hook(win_ptr, 33, 0, handle_close, (mlx, mlx_ptr))

    mlx.mlx_string_put(mlx_ptr, win_ptr, int(screen_width / 2), int(screen_height / 2) - 5, 0x00FFFFFF, "Hello world")

    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)

if __name__ == "__main__":
    main()
