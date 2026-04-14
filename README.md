*This project has been created as part of the 42 curriculum by [efiorent](https://github.com/ElioFiorentini) and [aginiaux](https://github.com/ExplorersPath).*
# Description

# Instructions
In order to launch our program, please activate a virtual environment, install the program dependencies, then launch the program.  
To activate a virtual environment:  
```bash
python3 -m venv a-maze-ing_venv
source a-maze-ing_venv/bin/activate
```  
To install the dependencies:  
```bash
make
```  
To run the program:  
```bash
python3 a_maze_ing.py config.txt
```
or:
```bash
make run CONF='config.txt'
```  

# Resources and tools used
AI was used to generate documentation about the `mlx`.  
We used [Wikipedia](wikipedia.org) for generation and solver algorithms.  
`flake8` and `mypy` for code consistency.  
## Algorithms
- [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) path finding algorithm  
- `Shape-maze-ster` generation algorithm ([aginiaux](https://github.com/ExplorersPath)'s creation)  

# Configuration file format
The configuration file must be organized as follow:
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

# Maze generation algorithm

# Task repartition


# Example of main
```
from maze_generator import MazeGenerator


if __name__ == "__main__":
    maze_generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0,0),
        exit=(5,5),
        output_file="maze.txt",
        perfect=True,
    )

    maze_generator.change_seed(42)

    maze_generator.chose_shape('triangle')

    maze = maze_generator.generate_full_maze()

    print(maze[0][0])

    solution = maze_generator.get_solution(maze)

    print(solution)
```
