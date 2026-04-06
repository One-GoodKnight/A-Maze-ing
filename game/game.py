from constants import *
from .player import Player
from maze_generator import Direction

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

    def gravity(self, player: Player):
        direction = None

        if ((self.angle >= 315 and self.angle <= 360) or (self.angle >= 0 and self.angle <= 45)):
            direction = Direction.SOUTH
        elif (self.angle >= 45 and self.angle <= 135):
            direction = Direction.EAST
        elif (self.angle >= 135 and self.angle <= 225):
            direction = Direction.NORTH
        else:
            direction = Direction.WEST
        
        match direction:
            case Direction.NORTH:
                player.y -= GRAVITY
            case Direction.EAST:
                player.x += GRAVITY
            case Direction.SOUTH:
                player.y += GRAVITY
            case Direction.WEST:
                player.x -= GRAVITY
            case _:
                pass
