from typing import List, Tuple

import networkx as nx

from graph.utils import GridCellType


def edge_list_to_graph(input_data: List[Tuple[int, int, int]]) -> nx.Graph:
    graph = nx.Graph()

    for u, v, weight in input_data:
        graph.add_edge(u, v, weight=weight)

    return graph


def graph_to_edge_list(graph: nx.Graph) -> List[Tuple[int, int, int]]:
    edges: List[Tuple[int, int, int]] = []
    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1.0)
        edges.append((weight, u, v))
    return edges


def grid_to_graph(input_data: List[List[GridCellType]]) -> nx.Graph:
    graph = nx.Graph()

    rows, cols = len(input_data), len(input_data[0])
    edges = [((i, j), (ni, nj), 1)
             for i in range(rows)
             for j in range(cols)
             for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
             if (input_data[i][j] != GridCellType.BLOCK
                 and 0 <= ni < rows
                 and 0 <= nj < cols
                 and input_data[ni][nj])]

    [graph.add_edge(node, neighbor, weight=weight)
     for node, neighbor, weight in edges]
    return graph


def graph_to_grid(graph: nx.Graph, width: int, height: int):
    maze = [[" " for _ in range(width)] for _ in range(height)]

    for node, data in graph.nodes(data=True):
        y, x = node
        if 'obstacle' in data and data['obstacle']:
            maze[y][x] = "#"
        elif 'weight' in data and data['weight'] > 1:
            maze[y][x] = "X"

    return maze


def find_char_location(maze: List[List[GridCellType]], wanted_char: GridCellType):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == wanted_char:
                return r, c
