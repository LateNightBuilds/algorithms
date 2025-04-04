def find_char_location(maze, wanted_char):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == wanted_char:
                return r, c
    return None