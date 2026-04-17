from constants import ROTATION_SPEED, AIR_DRAG, GRAVITY
from constants import PLAYER_BOUNCE, FRICTION
from .player import Player
from maze_generator import Cell
from .Vector2 import Vector2
from .state import State
import math


class Game():
    """
    Manages game variables with various utilities to handle
    rotations, player physics and collisions.
    """
    def __init__(self, maze_width: int, maze_height: int) -> None:
        """
        Initializes the game and sets various variables to default value.

        Att
        """
        self.start_loop_time: float = 0
        self.end_loop_time: float = 0
        self.deltatime: float = 0
        self.__angle: float = 0
        self.left_rotate: bool = False
        self.right_rotate: bool = False
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height
        self.state: State = State.INIT_GENERATION
        self.timer: float = 0

        self.iteration: int = 0
        self.last_fps: list[float] = []
        self.max_fps: float = 0
        self.min_fps: float = math.inf
        self.avg_fps: float = 0
        self.display_fps: bool = False

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        while (value < 0):
            value += 360

        self.__angle = value % 360

    def rotate(self, game_state: State) -> None:
        if game_state != State.PLAY:
            return
        direction = 0
        if (self.left_rotate):
            direction -= 1
        if (self.right_rotate):
            direction += 1
        self.angle += direction * ROTATION_SPEED * self.deltatime

    def wall_collisions(self, maze: list[list[Cell]],
                        cell_size: int, player: Player
                        ) -> tuple[bool, bool, bool, bool]:
        max_x = len(maze[0]) - 1
        max_y = len(maze) - 1

        def cell_at(pos: Vector2) -> Cell:
            y = math.floor(pos.y / cell_size)
            x = math.floor(pos.x / cell_size)
            return maze[y][x]

        top_left_cell = cell_at(player.top_left_corner)
        top_right_cell = cell_at(player.top_right_corner)
        bottom_left_cell = cell_at(player.bottom_left_corner)
        bottom_right_cell = cell_at(player.bottom_right_corner)

        direct_top_wall = top_left_cell.north or top_right_cell.north
        direct_east_wall = top_right_cell.east or bottom_right_cell.east
        direct_south_wall = bottom_left_cell.south or bottom_right_cell.south
        direct_west_wall = top_left_cell.west or bottom_left_cell.west

        # neighbor cell
        def n_cell(cell: Cell, offset: tuple[int, int]) -> Cell:
            return maze[cell.y + offset[1]][cell.x + offset[0]]

        x = player.x // cell_size
        y = player.y // cell_size
        ortho_top_wall = False
        if top_left_cell != top_right_cell and y > 0:
            top_top_left_cell = n_cell(top_left_cell, (0, -1))
            top_top_right_cell = n_cell(top_right_cell, (0, -1))
            ortho_top_wall = \
                top_top_left_cell.east or top_top_right_cell.west

        ortho_east_wall = False
        if top_right_cell != bottom_right_cell and x < max_x:
            top_right_right_cell = n_cell(top_right_cell, (1, 0))
            bottom_right_right_cell = n_cell(bottom_right_cell, (1, 0))
            ortho_east_wall = \
                top_right_right_cell.south or bottom_right_right_cell.north

        ortho_south_wall = False
        if bottom_left_cell != bottom_right_cell and y < max_y:
            bottom_bottom_left_cell = n_cell(bottom_left_cell, (0, 1))
            bottom_bottom_right_cell = n_cell(bottom_right_cell, (0, 1))
            ortho_south_wall = \
                bottom_bottom_left_cell.east or bottom_bottom_right_cell.west

        ortho_west_wall = False
        if top_left_cell != bottom_left_cell and x > 0:
            top_left_left_cell = n_cell(top_left_cell, (-1, 0))
            bottom_left_left_cell = n_cell(bottom_left_cell, (-1, 0))
            ortho_west_wall = \
                top_left_left_cell.south or bottom_left_left_cell.north

        return (
            direct_top_wall or ortho_top_wall,
            direct_east_wall or ortho_east_wall,
            direct_south_wall or ortho_south_wall,
            direct_west_wall or ortho_west_wall,
        )

    def gravity(self, maze: list[list[Cell]],
                cell_size: int, player: Player) -> None:
        rad = math.radians(self.angle)

        air_drag = Vector2(player.velocity.x * AIR_DRAG * self.deltatime,
                           player.velocity.y * AIR_DRAG * self.deltatime)
        player.velocity -= air_drag

        direction = Vector2(math.sin(rad), math.cos(rad))
        magnitude = math.sqrt(direction.x ** 2 + direction.y ** 2)
        normalized_dir = Vector2(direction.x / magnitude,
                                 direction.y / magnitude)

        move_vector = Vector2(normalized_dir.x * GRAVITY * self.deltatime,
                              normalized_dir.y * GRAVITY * self.deltatime)

        north_wall, east_wall, south_wall, west_wall = \
            self.wall_collisions(maze, cell_size, player)

        if (south_wall and (player.velocity.y + move_vector.y) > 0):
            cur_cell_y = math.floor(player.bottom_left_corner.y / cell_size)
            new_vel = player.velocity.y + move_vector.y
            tar_cell_y = math.floor(
                (new_vel + player.bottom_left_corner.y) / cell_size
            )
            if (cur_cell_y != tar_cell_y):
                player.y = (tar_cell_y * cell_size) - player.size + 0.999
                move_vector.y = 0
                player.velocity.y = min(0, -player.velocity.y * PLAYER_BOUNCE)
                friction = player.velocity.x * FRICTION * self.deltatime
                player.velocity.x -= friction

        if (north_wall and (player.velocity.y + move_vector.y) < 0):
            cur_cell_y = math.floor(player.top_left_corner.y / cell_size)
            new_vel = player.velocity.y + move_vector.y
            tar_cell_y = math.floor(
                (player.top_left_corner.y + new_vel) / cell_size
            )
            if (cur_cell_y != tar_cell_y):
                player.y = cur_cell_y * cell_size
                move_vector.y = 0
                player.velocity.y = max(0, -player.velocity.y * PLAYER_BOUNCE)
                friction = player.velocity.x * FRICTION * self.deltatime
                player.velocity.x -= friction

        player.velocity.y += move_vector.y
        player.y += player.velocity.y

        north_wall, east_wall, south_wall, west_wall = \
            self.wall_collisions(maze, cell_size, player)

        if (east_wall and (player.velocity.x + move_vector.x) > 0):
            cur_cell_x = math.floor(player.top_right_corner.x / cell_size)
            new_vel = player.velocity.x + move_vector.x
            tar_cell_x = math.floor(
                (player.top_right_corner.x + new_vel) / cell_size
            )
            if (cur_cell_x != tar_cell_x):
                player.x = (tar_cell_x * cell_size) - player.size + 0.999
                move_vector.x = 0
                player.velocity.x = min(0, -player.velocity.x * PLAYER_BOUNCE)
                friction = player.velocity.y * FRICTION * self.deltatime
                player.velocity.y -= friction

        if (west_wall and (player.velocity.x + move_vector.x) < 0):
            cur_cell_x = math.floor(player.top_left_corner.x / cell_size)
            new_vel = player.velocity.x + move_vector.x
            tar_cell_x = math.floor(
                (player.top_left_corner.x + new_vel) / cell_size
            )
            if (cur_cell_x != tar_cell_x):
                player.x = cur_cell_x * cell_size
                move_vector.x = 0
                player.velocity.x = max(0, -player.velocity.x * PLAYER_BOUNCE)
                friction = player.velocity.y * FRICTION * self.deltatime
                player.velocity.y -= friction

        player.velocity.x += move_vector.x
        player.x += player.velocity.x
