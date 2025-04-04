import heapq
import numpy as np

from typing import List, Tuple, Callable
from utils import find_char_location

class ShortestPathAlgorithms:
    def __init__(self, maze: List[List[int]], goal: Tuple[int, int]):
        self.maze = maze
        self.goal = goal
        
    def a_star_algorithm(self, h_n: Callable):
        return self._shortest_path_algorithm(h_n=h_n)
        
    def dijkstra_algorithm(self):
        h_n = lambda ny, nx: 0
        return self._shortest_path_algorithm(h_n=h_n)

    def _shortest_path_algorithm(self, h_n: Callable):

        num_of_steps = 0
        height, width = len(self.maze), len(self.maze[0])
        min_distances = np.full((height, width), np.inf)
        
        y_E, x_E = self.goal
        y_S, x_S = find_char_location(maze=self.maze, wanted_char="S")
        
        heap = [(0, y_S, x_S)]
        min_distances[y_S, x_S] = 0
        directions = [[0,1], [0,-1], [1,0], [-1,0]]
        
        g_n = lambda ny, nx: 4 if self.maze[ny][nx] == "X" else 1
        
        while(heap):
            num_of_steps += 1
            weight, y, x = heapq.heappop(heap)

            if x == x_E and y == y_E:
                return weight, num_of_steps
            
            neighbors = [(y + dy, x + dx) for dx, dy in directions
                        if 0 <= x + dx < width and 0 <= y + dy < height 
                        and self.maze[y + dy][x + dx] != "#"]
            
            for ny, nx in neighbors:
                g_val = min_distances[y, x] + g_n(ny=ny, nx=nx)   
                if g_val < min_distances[ny ,nx]:
                    min_distances[ny ,nx] = g_val
                    
                    h_val = h_n(ny=ny, nx=nx)
                    heapq.heappush(heap, (g_val + h_val, ny, nx))
                    
        return -1, num_of_steps


def main():
    maze = [
    ["S", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", "#", "#", "#", "#", ".", "#", "#", "#", "."],
    [".", "#", "X", "X", "#", ".", "#", "X", "#", "."],
    [".", "#", "X", "#", "#", ".", "#", "X", "#", "."],
    [".", "#", "X", "#", "#", ".", "#", "X", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
    [".", "#", "X", "#", "#", "#", "#", ".", "#", "."],
    [".", "#", "X", "#", "X", "X", "#", ".", "#", "."],
    [".", "#", "#", "#", "X", ".", ".", ".", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", "E"]
    ]
    
    goal = find_char_location(maze=maze, wanted_char="E")
    shortest_path_algorithm = ShortestPathAlgorithms(maze=maze, goal=goal)
    
    dijkstra_cost, dijkstra_num_of_steps = shortest_path_algorithm.dijkstra_algorithm()
    print(f"Dijkstra best cost: {dijkstra_cost}, found in {dijkstra_num_of_steps} steps.")
    
    y_E, x_E = goal
    h_n = lambda ny, nx: abs(ny - y_E) + abs(nx - x_E) 
    a_star_cost, a_star_num_of_steps = shortest_path_algorithm.a_star_algorithm(h_n=h_n)
    print(f"A_star best cost: {a_star_cost}, found in {a_star_num_of_steps} steps.")
    

if __name__ == "__main__":
    main()