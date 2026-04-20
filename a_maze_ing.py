try:
    from mlx import Mlx
except ImportError as e:
    raise SystemExit(f"Unable to import mlx: {e}")
from maze import Maze
from mazegen import MazeGenerator, Cell, \
    WallBuilder, solve
from display import Image, Font, MazeDisplay, set_logo_color, display_player, \
    highlight_solution, clear_solution, random_maze_logo_color, random_color
from helpers import CalculateSize, parse_logo
from game import Game, State, Player, check_end
from constants import Const
from typing import cast, Generator
from ctypes import c_void_p
from math import floor
from time import time


def display_generation(
    params: tuple[Mlx, c_void_p, c_void_p, Image, Maze, MazeDisplay]
) -> None:
    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display = params
    image.set_to(Const.BLACK)
    mlx_maze_display.display_maze(maze)
    image.rotate(0)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def display_play(
    params: tuple[Mlx, c_void_p, c_void_p, Image,
                  Maze, MazeDisplay, Game, Player]
) -> None:
    mlx, mlx_ptr, win_ptr, image, maze, mlx_maze_display, game, player = params

    mlx_maze_display.display_maze(maze)
    display_player(image, player)

    image.rotate(game.angle)

    if image.font is None:
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)
        return

    game.iteration += 1
    fps = int(1 // game.deltatime)
    if fps < game.min_fps:
        game.min_fps = fps
    if fps > game.max_fps:
        game.max_fps = fps
    if len(game.last_fps) >= 10:
        game.last_fps[game.iteration % 10] = fps
    game.avg_fps += fps
    if game.display_fps > 0:
        fps_text = f"{sum(game.last_fps) / len(game.last_fps):.0f} FPS"
        if game.display_fps > 1:
            fps_text += (
                f"\n{game.max_fps:.0f} max FPS\n"
                f"{game.min_fps:.0f} min FPS\n"
                f"{game.avg_fps // game.iteration:.0f} average FPS"
            )
        image.print(10, 10, fps_text, color=Const.WHITE, size=1)

    timer_text = f"Timer: {game.timer:.2f}s"
    if image.font is not None:
        image.print(
            0, -(image.height // 2) + (image.font.height * 3),
            timer_text, color=Const.WHITE, size=3, center=True
        )

    controls = (
        "Controls:\n"
        "  <h> to show the solution\n"
        "  <f> to show fps stats\n"
        "  <c> to randomize colors\n"
        "  <q> or <esc> to quit"
    )
    image.print(
        image.font.width,
        image.height - image.font.height * 2 * len(controls.splitlines()),
        controls, color=Const.WHITE, size=2
    )

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def display_end(params: tuple[Mlx, c_void_p, c_void_p, Image, Game]) -> None:
    mlx, mlx_ptr, win_ptr, image, game = params
    image.set_to(Const.BLACK)
    text = (
        "You won GG !!!\n\n"
        f"Finised in {game.timer:.2f}s\n\n"
        "Press R to generate a new maze"
    )
    image.print(0, 0, text, color=Const.WHITE, size=3, center=True)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, image.ptr, 0, 0)


def game_loop(
    params: tuple[Mlx, c_void_p, c_void_p, Image, MazeGenerator,
                  Maze, MazeDisplay, Game, Player, list[Cell]]
) -> None:
    game_start_loop_time = time()

    (mlx, mlx_ptr, win_ptr, image, maze_generator, maze,
     mlx_maze_display, game, player, logo) = params

    time_between_loops = game_start_loop_time - \
        (game.end_loop_time if game.end_loop_time != 0
         else game_start_loop_time)
    game.deltatime += time_between_loops
    game.start_loop_time = game_start_loop_time

    if game.state == State.INIT_GENERATION:
        maze_generator.gen = cast(
            Generator[list[list[Cell | None]], None, None],
            maze_generator.get_maze_generator(logo)
        )
        maze.player_solution = ''
        maze.cell_counter = 0
        maze.maze = [[None] * maze.width for _ in range(maze.height)]
        maze.init_time = time()
        game.state = State.GENERATION

    elif game.state == State.GENERATION:
        time_since_gen_start = time() - maze.init_time
        cells_that_should_be_generated = time_since_gen_start \
            / Const.ANIMATION_SPEED * maze.width * maze.height
        cells_that_should_be_generated_after_this_frame = \
            cells_that_should_be_generated + game.deltatime \
            / Const.ANIMATION_SPEED * maze.width * maze.height
        cells_to_generate = max(
            0,
            cells_that_should_be_generated_after_this_frame - maze.cell_counter
        )

        new_maze = None
        try_generate = False
        for i in range(floor(cells_to_generate)):
            try:
                try_generate = True
                new_maze = next(
                    cast(Generator[list[list[Cell]]], maze_generator.gen)
                )
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
            maze.solution = solve(
                cast(list[list[Cell]], maze.maze),
                maze.entry, maze.exit
            )
            try:
                maze_generator.build_output(cast(list[list[Cell]], maze.maze))
            except PermissionError:
                print(f"Cannot write to output '{maze.output_file}', "
                      "permission denied")
            game.state = State.INIT_PLAY
        else:
            if new_maze:
                maze.maze = cast(list[list[Cell | None]], new_maze)
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
            cast(list[list[Cell]], maze.maze),
            (int(player.center_x // maze.cell_size),
             int(player.center_y // maze.cell_size)),
            maze.exit
        )
        maze.show_solutions = False
        game.last_fps = [0 for _ in range(10)]
        # print(maze)
        maze_tmp = Maze.from_file('empty_maze.txt')
        maze.maze = maze_tmp.maze
        maze.width = maze_tmp.width
        maze.height = maze_tmp.height
        maze.cell_size = maze_tmp.cell_size
        maze.entry = maze_tmp.entry
        maze.exit = maze_tmp.exit


    elif game.state == State.PLAY:
        game.timer += game.deltatime

        game.rotate(game.state)

        prev_x, prev_y = (player.center_x // maze.cell_size,
                          player.center_y // maze.cell_size)
        game.gravity(cast(list[list[Cell]], maze.maze), maze.cell_size, player)
        new_x, new_y = (player.center_x // maze.cell_size,
                        player.center_y // maze.cell_size)

        if maze.show_solutions and (prev_x != new_x or prev_y != new_y):
            clear_solution(maze.maze, (
                int(prev_x), int(prev_y)
            ), maze.player_solution)
            highlight_solution(
                maze.maze, maze.entry, maze.solution, Const.MAZE_SOLUTION_COLOR
            )
            maze.player_solution = solve(
                cast(list[list[Cell]], maze.maze),
                (int(player.center_x // maze.cell_size),
                 int(player.center_y // maze.cell_size)),
                maze.exit
            )
            highlight_solution(maze.maze, (
                int(new_x), int(new_y)
            ), maze.player_solution, Const.MAZE_PLAYER_SOLUTION_COLOR)

        display_play((mlx, mlx_ptr, win_ptr, image,
                      maze, mlx_maze_display, game, player))
        if (check_end(player, maze.cell_size, maze.exit)):
            game.state = State.END

    elif game.state == State.END:
        display_end((mlx, mlx_ptr, win_ptr, image, game))

    game.deltatime = time() - game.start_loop_time
    game.end_loop_time = time()


def handle_key_press(
    keycode: int,
    params: tuple[Mlx, c_void_p, Game, MazeGenerator,
                  Image, Maze, Player, list[Cell]]
) -> None:
    mlx, mlx_ptr, game, maze_generator, image, maze, player, logo = params
    if keycode == 0xFF1B or keycode == ord('q'):
        mlx.mlx_loop_exit(mlx_ptr)

    if keycode == 0xff51:
        game.left_rotate = True
    if keycode == 0xff53:
        game.right_rotate = True

    if game.state == State.PLAY and keycode == ord('c'):
        random_maze_logo_color(cast(list[list[Cell]], maze.maze), logo)
        Const.MAZE_BORDER_COLOR = random_color()

    if game.state == State.END and keycode == ord('r'):
        game.state = State.INIT_GENERATION

    if game.state == State.PLAY and keycode == ord('h'):
        if maze.show_solutions:
            clear_solution(maze.maze, (
                int(player.center_x // maze.cell_size),
                int(player.center_y // maze.cell_size)
            ), maze.player_solution)
            clear_solution(maze.maze, maze.entry, maze.solution)
            maze.show_solutions = False
        else:
            highlight_solution(
                maze.maze, maze.entry, maze.solution, Const.MAZE_SOLUTION_COLOR
            )
            maze.player_solution = solve(cast(list[list[Cell]], maze.maze), (
                int(player.center_x // maze.cell_size),
                int(player.center_y // maze.cell_size)
            ), maze.exit)
            highlight_solution(maze.maze, (
                int(player.center_x // maze.cell_size),
                int(player.center_y // maze.cell_size)
            ), maze.player_solution, Const.MAZE_PLAYER_SOLUTION_COLOR)
            maze.show_solutions = True

    if game.state == State.PLAY and keycode == ord('f'):
        game.display_fps = (game.display_fps + 1) % 3


def handle_key_release(keycode: int, params: Game) -> None:
    game = params

    if keycode == 0xff51:
        game.left_rotate = False
    if keycode == 0xff53:
        game.right_rotate = False


def handle_close(params: tuple[Mlx, c_void_p]) -> None:
    mlx, mlx_ptr = params
    mlx.mlx_loop_exit(mlx_ptr)


def main() -> int:
    import sys

    argc = len(sys.argv)
    if argc != 2:
        print("The program should be run with: "
              "python3 a_maze_ing.py config_file_name")
        return 1

    filename = sys.argv[1]
    try:
        maze_generator = MazeGenerator.from_file(filename)
        filename = "logo.42"
        parse_logo_data = parse_logo(filename, maze_generator.width,
                                     maze_generator.height)

        logo: list[Cell]
        logo_width: int
        logo_height: int
        if parse_logo_data:
            logo, logo_width, logo_height = parse_logo_data
        else:
            logo, logo_width, logo_height = [], 0, 0
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
        too_big = ((logo_width + 2 > maze_generator.width) or
                   (logo_height + 2 > maze_generator.height))
        if (too_big):
            sys.stderr.write("Error, maze too small for the logo, "
                             "starting the maze without it.\n")
            logo = []

        temp_entry = Cell(x=maze_generator.entry[0], y=maze_generator.entry[1])
        temp_exit = Cell(x=maze_generator.exit[0], y=maze_generator.exit[1])
        if (isinstance(logo, list) and temp_entry in logo):
            sys.stderr.write("Error: entry on logo, "
                             "starting the maze without logo.\n")
            logo = []
        elif (isinstance(logo, list) and temp_exit in logo):
            sys.stderr.write("Error: exit on logo, "
                             "starting the maze without logo.\n")
            logo = []
    else:
        logo = []

    maze = Maze(**maze_generator.to_dict())

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    _, screen_width, screen_height = mlx.mlx_get_screen_size(mlx_ptr)
    window_width, window_height, maze.cell_size = \
        CalculateSize.calculate(screen_width, screen_height,
                                maze.width, maze.height)
    window_width, window_height = (window_width + 1, window_height + 1)
    win_ptr = mlx.mlx_new_window(mlx_ptr, window_width,
                                 window_height, "A-maze-ing")
    Const.MAZE_HYPO = CalculateSize.calculate_hypothenus(
            maze.width, maze.height)

    image = Image(mlx, mlx_ptr, window_width, window_height, font)
    mlx_maze_display = MazeDisplay(mlx, image)
    set_logo_color(logo)

    game = Game(maze.width, maze.height)
    player_size = int(maze.cell_size * Const.PLAYER_SIZE)
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
                 (mlx, mlx_ptr, game, maze_generator, image, maze,
                  player, logo))
    mlx.mlx_hook(win_ptr, key_release_event,
                 key_release_mask, handle_key_release,
                 (game))

    mlx.mlx_loop_hook(mlx_ptr, game_loop,
                      (mlx, mlx_ptr, win_ptr, image, maze_generator,
                       maze, mlx_maze_display, game, player, logo))

    mlx.mlx_loop(mlx_ptr)

    mlx.mlx_do_key_autorepeaton(mlx_ptr)
    mlx.mlx_destroy_image(mlx_ptr, image.ptr)
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_release(mlx_ptr)
    return 0


if __name__ == "__main__":
    main()
