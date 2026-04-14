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
