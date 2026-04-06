from constants import *
from .player import Player
from maze_generator import Cell, Direction
from typing import Tuple

class Game():
    def __init__(self, maze_width: int, maze_height: int):
        self.delta_time = 0
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
        self.angle += direction * ROTATION_SPEED * self.delta_time

    def should_stop(self, maze: list[list[Cell]], player: Player) -> Tuple[bool, float]:
        cell_x, cell_y = (player.center_x // player.size, player.center_y // player.size)
        cell = maze[int(cell_y)][int(cell_x)]

        if (not getattr(cell, player.direction)):
            return (False, 0)

        cell_size = player.size
        match player.direction:
            case Direction.NORTH:
                distance_to_wall = player.y - cell_y * cell_size
            case Direction.EAST:
                distance_to_wall = ((cell_x + 1) * cell_size) - (player.x + player.size)
            case Direction.SOUTH:
                distance_to_wall = ((cell_y + 1) * cell_size) - (player.y + player.size)
            case Direction.WEST:
                distance_to_wall = player.x - cell_x * cell_size
            case _:
                distance_to_wall = 0

        return (True, distance_to_wall)
    
    def can_change_direction(self, player: Player):
        cell_x, cell_y = (player.center_x // player.size, player.center_y // player.size)
        threshold = player.size / 100
        cell_size = player.size
        if (abs(player.x - cell_x * cell_size) > threshold):
            return False
        if (abs(player.y - cell_y * cell_size) > threshold):
            return False
        return True

    def gravity(self, maze: list[list[Cell]], player: Player):
        direction = None

        if ((self.angle >= 315 and self.angle <= 360) or (self.angle >= 0 and self.angle <= 45)):
            direction = Direction.SOUTH
            if (self.angle >= 315):
                avg_angle = 360
            else:
                avg_angle = 0
        elif (self.angle >= 45 and self.angle <= 135):
            direction = Direction.EAST
            avg_angle = (45 + 135) / 2
        elif (self.angle >= 135 and self.angle <= 225):
            direction = Direction.NORTH
            avg_angle = (135 + 225) / 2
        else:
            direction = Direction.WEST
            avg_angle = (225 + 315) / 2

        print(self.can_change_direction(player))
        if (direction != player.direction and self.can_change_direction(player)):
            player.direction = direction

        angle_offset = abs(self.angle - avg_angle)
        offset_percent = angle_offset / 45
        force_with_friction = GRAVITY * (1 - offset_percent)

        stop, distance_to_wall = self.should_stop(maze, player)

        if (stop and force_with_friction * self.delta_time > distance_to_wall):
            force_with_friction = distance_to_wall
        else:
            stop = False

        match direction:
            case Direction.NORTH:
                player.y -= force_with_friction * (self.delta_time if not stop else 1)
            case Direction.EAST:
                player.x += force_with_friction * (self.delta_time if not stop else 1)
            case Direction.SOUTH:
                player.y += force_with_friction * (self.delta_time if not stop else 1)
            case Direction.WEST:
                player.x -= force_with_friction * (self.delta_time if not stop else 1)
            case _:
                pass
