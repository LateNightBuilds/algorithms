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
    g = nx.Graph()
    rows = len(input_data)
    cols = len(input_data[0]) if rows > 0 else 0

    edges = [((i, j), (ni, nj), input_data[ni][nj])
             for i in range(rows)
             for j in range(cols)
             for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
             if (input_data[i][j] != GridCellType.BLOCK
                 and 0 <= ni < rows
                 and 0 <= nj < cols
                 and input_data[ni][nj])]

    all_nodes = set()
    for (u, v, weight) in edges:
        all_nodes.add(u)
        all_nodes.add(v)

    for node in all_nodes:
        row, col = node
        node_data = {"row": row, "col": col, "cell_type": input_data[row][col]}
        g.add_node(node, **node_data)

    g.add_weighted_edges_from([(u, v, weight) for u, v, weight in edges])

    return g


def graph_to_grid(graph):
    if not graph.nodes:
        return []

    max_row = -1
    max_col = -1
    for node, data in graph.nodes(data=True):
        max_row = max(max_row, data['row'])
        max_col = max(max_col, data['col'])

    rows = max_row + 1
    cols = max_col + 1
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    for node, data in graph.nodes(data=True):
        row = data['row']
        col = data['col']
        grid_value = data.get('cell_type', node)
        grid[row][col] = grid_value

    return grid


def find_char_location(maze: List[List[GridCellType]], wanted_char: GridCellType):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == wanted_char:
                return r, c
