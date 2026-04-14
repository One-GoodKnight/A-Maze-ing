try:
    from mlx import Mlx
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from maze import Maze
from maze_generator import MazeGenerator, Cell, \
    WallBuilder, solve
from parsing import parse_config_file, parse_logo
from display import Image, Font, MazeDisplay, set_logo_color, display_player, \
    highlight_solution, clear_solution
from helpers import CalculateSize
from game import Game, State, Player, check_end
from constants import WHITE, BLACK, PLAYER_SIZE, ANIMATION_SPEED, \
    MAZE_SOLUTION_COLOR, MAZE_PLAYER_SOLUTION_COLOR
import random
import time
import math


def display_generation(params):
    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display = params
    image.set_to(BLACK)
    mlx_maze_display.display_maze(maze, 0, 0)
    image.rotate(0)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def display_play(params):
    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player = params

    mlx_maze_display.display_maze(maze, 0, 0)
    display_player(image, player)

    image.rotate(game.angle)

    rot = f"Maze rotation: {game.angle:06.2f} degree"
    image.print(10, 10, rot, color=WHITE, bg_color=None, size=3)

    timer = f"Timer: {game.timer:.2f}s"
    image.print(10, image.height - 45, timer, color=WHITE, bg_color=None, size=3)

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def display_end(params):
    mlx, mlx_ptr, win_ptr, image, game = params
    image.set_to(BLACK)
    text = f"GG - {game.timer:.2f}s - Press R to generate a new maze"
    image.print(-1, -1, text, color=WHITE, size=4)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def game_loop(params):
    game_start_loop_time = time.time()

    (mlx, mlx_ptr, win_ptr, image, maze_generator, maze,
     mlx_maze_display, game, player, logo) = params

    time_between_loops = game_start_loop_time - \
        (game.end_loop_time if game.end_loop_time != 0
         else game_start_loop_time)
    game.deltatime += time_between_loops
    game.start_loop_time = game_start_loop_time

    if game.state == State.INIT_GENERATION:
        maze_generator.gen = maze_generator.get_maze_generator(logo)
        maze.player_solution = ''
        maze.cell_counter = 0
        maze.maze = [[None] * maze.width for _ in range(maze.height)]
        maze.init_time = time.time()
        game.state = State.GENERATION

    elif game.state == State.GENERATION:
        time_since_gen_start = time.time() - maze.init_time
        cells_that_should_be_generated = time_since_gen_start \
            / ANIMATION_SPEED * maze.width * maze.height
        cells_that_should_be_generated_after_this_frame = \
            cells_that_should_be_generated + game.deltatime \
            / ANIMATION_SPEED * maze.width * maze.height
        cells_to_generate = max(
            0,
            cells_that_should_be_generated_after_this_frame - maze.cell_counter
        )

        new_maze = None
        try_generate = False
        for i in range(math.floor(cells_to_generate)):
            try:
                try_generate = True
                new_maze = next(maze_generator.gen)
                if not new_maze:
                    break
                maze.cell_counter += 1
            except StopIteration as e:
                print("An error occurred during the "
                      f"generation of the maze: {e}")
            except Exception as e:
                print("An error occurred during the "
                      f"generation of the maze: {e}")
        if try_generate and not new_maze:
            maze.solution = solve(maze.maze, maze.entry, maze.exit)
            try:
                maze_generator.build_output(maze.maze)
            except PermissionError:
                print(f"Cannot write to output '{maze.output_file}', "
                      "permission denied")
            game.state = State.INIT_PLAY
        else:
            if new_maze:
                maze.maze = new_maze
                WallBuilder.build_wall(maze.maze)
            display_generation((mlx, mlx_ptr, win_ptr,
                                image, maze, mlx_maze_display))

    elif game.state == State.INIT_PLAY:
        player.x, player.y = (maze.entry[0] * maze.cell_size,
                              maze.entry[1] * maze.cell_size)
        player.velocity.x, player.velocity.y = (0, 0)
        game.angle = 0
        game.deltatime = 0
        game.timer = 0
        game.state = State.PLAY
        maze.player_solution = solve(
            maze.maze,
            (int(player.center_x // maze.cell_size),
             int(player.center_y // maze.cell_size)),
            maze.exit
        )
        maze.show_solutions = False

    elif game.state == State.PLAY:
        game.timer += game.deltatime

        game.rotate(game.state)

        prev_x, prev_y = (player.center_x // maze.cell_size,
                          player.center_y // maze.cell_size)
        game.gravity(maze.maze, maze.cell_size, player)
        new_x, new_y = (player.center_x // maze.cell_size,
                        player.center_y // maze.cell_size)

        if maze.show_solutions and (prev_x != new_x or prev_y != new_y):
            clear_solution(image, maze.maze,
                           (int(prev_x), int(prev_y)), maze.player_solution)
            # highlight solution from maze entry back after clear
            # for when the player was on
            highlight_solution(image, maze.maze, maze.entry,
                               maze.solution, MAZE_SOLUTION_COLOR)
            maze.player_solution = solve(
                maze.maze,
                (int(player.center_x // maze.cell_size),
                 int(player.center_y // maze.cell_size)),
                maze.exit
            )
            highlight_solution(image, maze.maze,
                               (int(new_x), int(new_y)),
                               maze.player_solution,
                               MAZE_PLAYER_SOLUTION_COLOR)

        display_play((mlx, mlx_ptr, win_ptr, image,
                      maze, mlx_maze_display, game, player))
        if (check_end(player, maze.cell_size, maze.exit)):
            game.state = State.END

    elif game.state == State.END:
        display_end((mlx, mlx_ptr, win_ptr, image, game))

    game.deltatime = time.time() - game.start_loop_time
    game.end_loop_time = time.time()


def handle_key_press(keycode, params):
    mlx, mlx_ptr, game, maze_generator, image, maze, player = params
    if keycode == 0xFF1B or keycode == ord('q'):
        mlx.mlx_loop_exit(mlx_ptr)

    if keycode == 0xff51:
        game.left_rotate = True
    if keycode == 0xff53:
        game.right_rotate = True

    if game.state == State.END and keycode == ord('r'):
        game.state = State.INIT_GENERATION

    if game.state == State.PLAY and keycode == ord('h'):
        if maze.show_solutions:
            clear_solution(image, maze.maze,
                           (int(player.center_x // maze.cell_size),
                            int(player.center_y // maze.cell_size)),
                           maze.player_solution)
            clear_solution(image, maze.maze, maze.entry, maze.solution)
            maze.show_solutions = False
        else:
            highlight_solution(image, maze.maze, maze.entry,
                               maze.solution, MAZE_SOLUTION_COLOR)
            maze.player_solution = solve(
                maze.maze,
                (int(player.center_x // maze.cell_size),
                 int(player.center_y // maze.cell_size)),
                maze.exit)
            highlight_solution(image, maze.maze,
                               (int(player.center_x // maze.cell_size),
                                int(player.center_y // maze.cell_size)),
                               maze.player_solution,
                               MAZE_PLAYER_SOLUTION_COLOR)
            maze.show_solutions = True


def handle_key_release(keycode, params):
    mlx, mlx_ptr, game, image, maze, player = params

    if keycode == 0xff51:
        game.left_rotate = False
    if keycode == 0xff53:
        game.right_rotate = False


def handle_close(params):
    mlx, mlx_ptr = params
    mlx.mlx_loop_exit(mlx_ptr)


def main() -> None:
    import sys

    argc = len(sys.argv)
    if argc != 2:
        print("The program should be run with: python3 a_maze_ing.py config_file_name")
        return 1

    config = {}
    filename = sys.argv[1]
    try:
        config = parse_config_file(filename)
        random.seed(config['seed'] if 'seed' in config else 42)
        filename = "logo.42"
        parse_logo_data = parse_logo(filename, config['width'],
                                     config['height'])
        logo, logo_width, logo_height = \
            parse_logo_data if parse_logo_data else (None, None, None)
    except FileNotFoundError:
        print(f"Could not find the file '{filename}'")
        return 1
    except PermissionError:
        print(f"Cannot read config file '{filename}', permission denied")
        return 1
    except Exception as e:
        print(f"An error occured during file parsing: {e}")
        return 1
    fontname = 'display/DeterminationMono'
    try:
        font = Font(fontname)
    except FileNotFoundError:
        print(f"Could not find the file '{fontname}'")
        return 1
    except PermissionError:
        print(f"Cannot read font file '{fontname}', permission denied")
        return 1
    except Exception as e:
        print(f"An error occured during file parsing: {e}")
        return 1

    if logo:
        too_big = ((logo_width + 2 > config['width']) or
                   (logo_height + 2 > config['height']))
        if (too_big):
            sys.stderr.write("Error, maze too small for the logo, "
                             "starting the maze without it.\n")
            logo = []

        temp_entry = Cell(x=config['entry'][0], y=config['entry'][1])
        temp_exit = Cell(x=config['exit'][0], y=config['exit'][1])
        if (temp_entry in logo):
            sys.stderr.write("Error: entry on logo, "
                             "starting the maze without logo.\n")
            logo = []
        elif (temp_exit in logo):
            sys.stderr.write("Error: exit on logo, "
                             "starting the maze without logo.\n")
            logo = []
    else:
        logo = []

    maze_generator = MazeGenerator(**config)

    maze = Maze(
        maze=None,
        solution="",
        width=maze_generator.width,
        height=maze_generator.height,
        entry=maze_generator.entry,
        exit=maze_generator.exit,
        output_file=maze_generator.output_file,
        perfect=maze_generator.perfect,
        player_solution="",
        show_solutions=False
    )

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    _, screen_width, screen_height = mlx.mlx_get_screen_size(mlx_ptr)
    window_width, window_height, maze.cell_size = \
        CalculateSize.calculate(screen_width, screen_height,
                                maze.width, maze.height)
    window_width, window_height = (window_width + 1, window_height + 1)
    win_ptr = mlx.mlx_new_window(mlx_ptr, window_width,
                                 window_height, "A-maze-ing")

    image = Image(mlx, mlx_ptr, window_width, window_height, font)
    mlx_maze_display = MazeDisplay(mlx, image)
    set_logo_color(image, logo)

    game = Game(maze.width, maze.height)
    player_size = int(maze.cell_size * PLAYER_SIZE)
    player = Player(maze.entry[0], maze.entry[1],
                    player_size, image.width,
                    image.height, maze.cell_size)

    mlx.mlx_do_key_autorepeatoff(mlx_ptr)

    client_message_event = 33
    mlx.mlx_hook(win_ptr, client_message_event, 0,
                 handle_close, (mlx, mlx_ptr))

    key_press_event, key_press_mask = (2, 1)
    key_release_event, key_release_mask = (3, 2)
    mlx.mlx_hook(win_ptr, key_press_event, key_press_mask, handle_key_press,
                 (mlx, mlx_ptr, game, maze_generator, image, maze, player))
    mlx.mlx_hook(win_ptr, key_release_event,
                 key_release_mask, handle_key_release,
                 (mlx, mlx_ptr, game, image, maze, player))

    game.time = time.time()

    mlx.mlx_loop_hook(mlx_ptr, game_loop,
                      (mlx, mlx_ptr, win_ptr, image, maze_generator,
                       maze, mlx_maze_display, game, player, logo))

    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_do_key_autorepeaton(mlx_ptr)
    mlx.mlx_destroy_image(mlx_ptr, image.ptr)
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)


if __name__ == "__main__":
    main()
