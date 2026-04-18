from mazegen import MazeGenerator


if __name__ == '__main__':
    maze_generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(1, 1),
        output_file='maze.txt',
        perfect=True,
    )

    maze_generator.change_seed(42)

    maze_generator.chose_shape('triangle')
    maze = maze_generator.generate_full_maze()

    solution = maze_generator.get_solution(maze)

    print("Maze:")
    print(maze)

    print("\nSolution:")
    print(solution)
