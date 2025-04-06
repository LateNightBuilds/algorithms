from typing import List, Set, Dict, Optional
from collections import deque

from utils import (GraphEdge, GraphNode, 
                   edges_list_to_adjacency_list, 
                   edges_list_to_nodes_set, 
                   print_nodes)

class BreadthFirstSearch:
    def __init__(self, edges: List[GraphEdge]):
        self.edges = edges
        self.nodes: Set[GraphNode] = edges_list_to_nodes_set(edges=self.edges)
        self.adjacency_list: Dict[GraphNode, List[GraphNode]] = (
            edges_list_to_adjacency_list(edges=self.edges))
        
    def is_connected(self, start_node: GraphNode) -> bool:
        queue = deque([(start_node, 1.0)])
        graph = self.adjacency_list
        visit_set: Set[GraphNode] = set()
        
        while queue:
            node, weight = queue.popleft()
            if node in visit_set:
                continue
            
            visit_set.add(node)
            
            for next_node in graph.get(node, []):
                queue.append(next_node)
                
        return visit_set == self.nodes
    
    def find_path(self, start_node: GraphNode, target_node: GraphNode) -> List[GraphNode]:
        queue = deque([(start_node, 1.0)])
        graph = self.adjacency_list
        parent = {start_node: None}
        visited = set([start_node])

        while queue:
            node, weight = queue.popleft()

            if node == target_node:
                break

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    neighbor_node, neighbor_weight = neighbor
                    visited.add(neighbor)
                    parent[neighbor_node] = node
                    queue.append(neighbor)

        if target_node not in parent:
            return None

        path = []
        current = target_node
        while current:
            path.append(current)
            current = parent[current]

        return path[::-1]
                

def main():
    edges = [(GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=1))), 
             (GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=2))), 
             (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=3))), 
             (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=4))), 
             (GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=5)))]
    
    bfs = BreadthFirstSearch(edges=edges)
    result = bfs.is_connected(start_node=GraphNode(value=0))
    print("Graph Connectivity:", result)
    
    path = bfs.find_path(start_node=GraphNode(value=0), target_node=GraphNode(value=4))
    if path:
        print_nodes(path)


if __name__ == "__main__":
    main()