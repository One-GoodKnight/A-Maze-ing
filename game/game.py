from constants import *
from .player import Player
from maze_generator import Cell, Direction
from .Vector2 import Vector2
from typing import Tuple
import math
import sys

class Game():
    def __init__(self, maze_width: int, maze_height: int):
        self.deltatime = 0
        self.__angle = 0
        self.left_rotate = False
        self.right_rotate = False
        self.maze_width = maze_width
        self.maze_height = maze_height

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        while (value < 0):
            value += 360

        self.__angle = value % 360

    def rotate(self) -> None:
        direction = 0
        if (self.left_rotate):
            direction -= 1
        if (self.right_rotate):
            direction += 1
        self.angle += direction * ROTATION_SPEED * self.deltatime

    def wall_collisions(self, maze: list[list[Cell]], cell_size: int, player: Player) -> Tuple[bool, bool, bool, bool]:
        top_left_cell = maze[math.floor(player.top_left_corner.y / cell_size)][math.floor(player.top_left_corner.x / cell_size)]
        top_right_cell = maze[math.floor(player.top_right_corner.y / cell_size)][math.floor(player.top_right_corner.x / cell_size)]
        bottom_left_cell = maze[math.floor(player.bottom_left_corner.y / cell_size)][math.floor(player.bottom_left_corner.x / cell_size)]
        bottom_right_cell = maze[math.floor(player.bottom_right_corner.y / cell_size)][math.floor(player.bottom_right_corner.x / cell_size)]
        center_cell = maze[math.floor(player.center_y / cell_size)][math.floor(player.center_x / cell_size)]

        return (
            (top_left_cell != top_right_cell or top_left_cell.north or (top_left_cell != center_cell)),
            (top_right_cell != bottom_right_cell or top_right_cell.east or (top_right_cell != center_cell)),
            (bottom_left_cell != bottom_right_cell or bottom_left_cell.south or (bottom_left_cell != center_cell)),
            (top_left_cell != bottom_left_cell or top_left_cell.west or (top_left_cell != center_cell)),
        )

    def gravity(self, maze: list[list[Cell]], cell_size: int, player: Player) -> None:
        rad = math.radians(self.angle)

        direction = Vector2(math.sin(rad), math.cos(rad))
        magnitude = math.sqrt(direction.x ** 2 + direction.y ** 2)
        normalized_dir = Vector2(direction.x / magnitude, direction.y / magnitude)

        move_vector = Vector2(normalized_dir.x * GRAVITY * self.deltatime, normalized_dir.y * GRAVITY * self.deltatime)

        north_wall, east_wall, south_wall, west_wall = self.wall_collisions(maze, cell_size, player)

        if (south_wall and (player.velocity.y + move_vector.y) > 0):
            cur_cell_y = math.floor(player.bottom_left_corner.y / cell_size)
            tar_cell_y = math.floor((player.bottom_left_corner.y + (player.velocity.y + move_vector.y)) / cell_size)
            if (cur_cell_y != tar_cell_y):
                player.y = (tar_cell_y * cell_size) - player.size + 0.7
                move_vector.y = 0
                player.velocity.y = 0

        if (north_wall and (player.velocity.y + move_vector.y) < 0):
            cur_cell_y = math.floor(player.top_left_corner.y / cell_size)
            tar_cell_y = math.floor((player.top_left_corner.y + (player.velocity.y + move_vector.y)) / cell_size)
            if (cur_cell_y != tar_cell_y):
                player.y = cur_cell_y * cell_size
                move_vector.y = 0
                player.velocity.y = 0

        player.velocity.y += move_vector.y
        player.y += player.velocity.y

        north_wall, east_wall, south_wall, west_wall = self.wall_collisions(maze, cell_size, player)

        if (east_wall and (player.velocity.x + move_vector.x) > 0):
            cur_cell_x = math.floor(player.top_right_corner.x / cell_size)
            tar_cell_x = math.floor((player.top_right_corner.x + (player.velocity.x + move_vector.x)) / cell_size)
            if (cur_cell_x != tar_cell_x):
                player.x = (tar_cell_x * cell_size) - player.size + 0.7
                move_vector.x = 0
                player.velocity.x = 0

        if (west_wall and (player.velocity.x + move_vector.x) < 0):
            cur_cell_x = math.floor(player.top_left_corner.x / cell_size)
            tar_cell_x = math.floor((player.top_left_corner.x + (player.velocity.x + move_vector.x)) / cell_size)
            if (cur_cell_x != tar_cell_x):
                player.x = cur_cell_x * cell_size
                move_vector.x = 0
                player.velocity.x = 0

        player.velocity.x += move_vector.x
        player.x += player.velocity.x
