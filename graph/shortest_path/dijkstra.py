import heapq
from typing import List, Tuple

import numpy as np

from graph.utils import (find_char_location,
                         GridCellType)
from graph.utils.history import HistoryLogger


class Dijkstra:
    def __init__(self, maze: List[List[GridCellType]]):
        self.maze = maze
        self.height, self.width = len(self.maze), len(self.maze[0])
        self.history = HistoryLogger()

        self.start_point = find_char_location(maze=self.maze, wanted_char=GridCellType.START)
        self.goal_point = find_char_location(maze=self.maze, wanted_char=GridCellType.END)

    def run(self) -> Tuple[int, HistoryLogger]:
        min_distances = np.full((self.height, self.width), np.inf)

        y_s, x_s = self.start_point
        y_e, x_e = self.goal_point

        heap = [(0, y_s, x_s)]
        min_distances[y_s, x_s] = 0
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        g_n = lambda g_y, g_x: 4 if self.maze[g_y][g_x] == GridCellType.OBSTACLE else 1

        while heap:
            weight, y, x = heapq.heappop(heap)
            self.history.add_new_step((y, x))

            if x == x_e and y == y_e:
                return weight, self.history

            neighbors = [(y + dy, x + dx) for dx, dy in directions
                         if 0 <= x + dx < self.width and 0 <= y + dy < self.height
                         and self.maze[y + dy][x + dx] != GridCellType.BLOCK]

            for n_y, n_x in neighbors:
                g_val = min_distances[y, x] + g_n(g_y=n_y, g_x=n_x)
                if g_val < min_distances[n_y, n_x]:
                    min_distances[n_y, n_x] = g_val
                    heapq.heappush(heap, (g_val, n_y, n_x))

        return -1, self.history
