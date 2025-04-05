from typing import List, Dict, Set
from . import GraphEdge, GraphNode
from collections import defaultdict

def find_char_location(maze, wanted_char):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == wanted_char:
                return r, c
    return None

def edges_list_to_adjacency_list(edges: List[GraphEdge]) -> Dict[GraphNode, List[GraphNode]]:
    adjacency_list: Dict[GraphNode, List[GraphNode]] = defaultdict(list)
    [adjacency_list[edge.from_node].append((edge.to_node, edge.weight)) for edge in edges]
    return adjacency_list

def edges_list_to_nodes_set(edges: List[GraphEdge]) -> Set[GraphNode]:
    return {node
            for edge in edges
            for node in [edge.from_node, edge.to_node]}