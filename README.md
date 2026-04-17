*This project has been created as part of the 42 curriculum by [efiorent](https://github.com/ElioFiorentini) and [aginiaux](https://github.com/ExplorersPath).*
# Description
The goal of the project is to create maze generator with some sort of a visualizer.  
The program must be able to handle a configuration file with multiple parameters for the maze generation.  
A pattern '42' should appear in the middle of the maze.  
Once the maze has been generated, it must be written in an output file in hex, with a solution to complete the maze.

The generation logic must be reusable by using a single class 'MazeGenerator' provided by in a module.

# Instructions
In order to launch our program, please activate a virtual environment, install the program dependencies, then launch the program.  
To activate a virtual environment:  
```bash
python3 -m venv a-maze-ing_venv
source a-maze-ing_venv/bin/activate
```  
To install the dependencies:  
```bash
make install
```  
To run the program:
```bash
python3 a_maze_ing.py config.txt
```
or:
```bash
make run
```  

# Resources and tools used
AI was used for:
- Generating a documentation about the `mlx`.
- Explaining concepts about algos / maths or libs like numpy
- Find alternatives to an existing solution to improve readability / use better suited built ins of the language
- Helping on debugging

We used [Wikipedia](wikipedia.org) for generation and solver algorithms.  
`flake8` and `mypy` for code consistency.  
## Algorithms
- [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) path finding algorithm  
- `Shape-mazester` generation algorithm ([aginiaux](https://github.com/ExplorersPath)'s creation)  
- [DDA](https://en.wikipedia.org/wiki/Digital_differential_analyzer_(graphics_algorithm)) raycasting algorithm

## Librairies
- Mlx as the graphical / hooking librairy
- [Numpy](https://numpy.org/) for rewriting the data of the mlx canvas faster
- [CV2] (https://pypi.org/project/opencv-python/) for the rotation of the maze

# Configuration file format
The configuration file must be organized as follow:

KEY=value
```text
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=0,4
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=-12
SHAPE=circle
```

All those keys are mandatory

The config file names allowed are *.txt

# Maze generation algorithm
The generation algorithm used is the famous Shape-mazester, it's an algo capable of generating mazes following simple geometric 2d shapes like circles, squares or triangles.

The algo starts at a random position and uses a shape generator to get an angle at which cast a ray-cast from the starting cell.  
If it finds an empty cell, it generates a neighbor from the cell just before, so a cell already inside the maze.  
It picks a direction depending on the current angle of the ray-cast, it only generates the neighbor if  
it is an empty cell, if it's not, it checks the next direction.

This repeats until the maze is full, at each ray-cast, the angle is incremented so that the consecutive
ray-casts follow a clock-wise rotation.

Shapes implemented are: circle, square and triangle.

I chose this algo because everyone did DFS and it's boring, also I wanted to see if it could work and it did so that's cool.
It's not really efficient tho but since we have a game on top of it we still had to limit the maze size to  
have a decent frame-rate.

# Feature list
For the mandatory:
- Config file parsing
- Maze generation
- Perfect / not perfect mazes
- Output file
- Visual representation

For the bonuses:
- Our own font class to change the font and the size of the font
- A playable character
- Gravity, collisions for the player
- bounce, air drag, friction
- A maze generation animation
- A generation algo that can use multiple shapes for the generation
- The keys SHAPE and SEED in the config file
- Display of the ray-cast during the generation
- Rotation of the maze that affects the gravity and collisions of the player
- A timer
- States to manage the state of the app
- a hotkey to highlight the solutions, one form the start and one from the player
- a check for the ending
- An end screen with a summary of informations
- A replay key to regenerate the maze and replay until the end of time
- A customizable pattern with logo.42
- Auto size of the window relative to the maze size
- A constant file to customize:
- MAZE_SCALE, ANIM_SPEED, BORDER_WIDTH, ROTATION_SPEED, COLORS, GRAVITY, BOUNCE, AIR_DRAG, FRICTION

# Technical choices
MAX_SIZE 50x50:
The main limit of our project is the maze size which we limited to 50x50.  
Two reasons for that, the first is the shape-mazester algorithm which is not suited for big mazes.
The other is the frame-rate at which the game runs, even with numpy, the game runs at about 40fps on  
a 50x50 maze on our mac.  
The maze has to be redrawn entirely every frame because of the rotation, this redrawn is the most impactful  
resource demanding functionality in the main loop.

Pydantic:
We used pydantic to validate the data of the config file to ensure the data valid.

Pip install:
pip for the dependencies, it's simple and effective

# Reusable code
The reusable code is the module maze_generator in which there is a MazeGenerator class that let's you use:
- Parsing for the config file
- The shape-mazester algo
- The solver

A main example to have a quick setup for the module is available at the end of this file.

# Project Management
## Roles of each member
Communicate and work on the discussed assigned tasks that are in the task repartition.

## Your anticipated planning and how it evolved until the end
We didn't plan much, we divided the tasks as the project advanced and since Elio was not here for a few days i did bonuses and he did the solver when he came back then we did the polish together.

## What worked well and what could be improved
### What worked well:
The repartition on independent functionalities really facilitated the work since we didn't had much conflicts between each other.

### What could be improved
The project was not really clear on what should be inside the module so we had to refactor multiple times to put what was needed inside and make it independant.  
Having a pydantic class specifically for the input validation would probably have been better, our class
contains variables that don't need to be validated but still are.
We should had taken more time on the project architecture at the beginning.

The main is a big fat, we could have divide it in multiple files.
Some methods / classes are a bit messy and could have been cleaned up.
We should have focused on flakes and mypy since the start it was tedious to resolve all the errors at the end.


# Task repartition

parsing: Alexandre
display: Elio, Alexandre
font: Elio
shape-mazester: Alexandre
solver: Elio
game: Alexandre
main: Alexandre, Elio
readme: Elio, Alexandre

# Example of main
```
from maze_generator import MazeGenerator


if __name__ == '__main__':
    maze_generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0,0),
        exit=(5,5),
        output_file='maze.txt',
        perfect=True,
    )
    maze_generator.change_seed(42)
    maze_generator.chose_shape('triangle')
    maze = maze_generator.generate_full_maze()
    maze_generator.build_output(maze)
    print(f'Maze saved in {maze_generator.output_file}')
```
