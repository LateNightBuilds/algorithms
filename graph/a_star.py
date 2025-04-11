import heapq
from typing import List

import numpy as np

from graph.utils import GridCellType, find_char_location


class AStar:
    def __init__(self, maze: List[List[GridCellType]]):
        self.maze = maze
        self.height, self.width = len(self.maze), len(self.maze[0])

        self.start_point = find_char_location(maze=self.maze, wanted_char=GridCellType.START)
        self.goal_point = find_char_location(maze=self.maze, wanted_char=GridCellType.END)

    def run(self, heuristic_func=None):
        num_of_steps = 0
        min_distances = np.full((self.height, self.width), np.inf)

        x_s, y_s = self.start_point
        x_e, y_e = self.goal_point

        if heuristic_func is None:
            h_n = lambda ny, nx: abs(ny - y_e) + abs(nx - x_e)  # noqa
        else:
            h_n = heuristic_func

        heap = [(0, y_s, x_s)]
        min_distances[y_s, x_s] = 0
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        g_n = lambda ny, nx: 4 if self.maze[ny][nx] == GridCellType.OBSTACLE else 1  # noqa

        while heap:
            num_of_steps += 1
            _, y, x = heapq.heappop(heap)

            if x == x_e and y == y_e:
                return min_distances[y_e, x_e], num_of_steps

            neighbors = [(y + dy, x + dx) for dx, dy in directions
                         if 0 <= x + dx < self.width and 0 <= y + dy < self.height
                         and self.maze[y + dy][x + dx] != GridCellType.BLOCK]

            for n_y, n_x in neighbors:
                g_val = min_distances[y, x] + g_n(ny=n_y, nx=n_x)
                if g_val < min_distances[n_y, n_x]:
                    min_distances[n_y, n_x] = g_val
                    h_val = h_n(ny=n_y, nx=n_x)
                    heapq.heappush(heap, (g_val + h_val, n_y, n_x))

        return -1, num_of_steps
