from typing import List, Set
from collections import defaultdict

from utils import GraphEdge, GraphNode

class DFS:
    
    def __init__(self, edges: List[GraphEdge]):
        self.edges = edges
        self.nodes = {node for edge in edges 
                      for node in [edge.from_node, edge.to_node]}

        self.graph = defaultdict(list)
        [self.graph[edge.from_node].append(edge.to_node) for edge in self.edges]
    
    def run(self, start_node: GraphNode):
        
        graph = self.graph
        visited_set: Set = set()
        
        def dfs(at: GraphNode):            
            if at in visited_set:
                return False

            visited_set.add(at)
            
            for next_node in graph.get(at, []):
                if not dfs(next_node): 
                    return False
        
            return True
        
        return dfs(at=start_node) and len(visited_set) == len(self.nodes)
        
    
if __name__ == "__main__":
    edges = [(GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=1))), 
             (GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=2))), 
             (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=3))), 
             (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=4))), 
             (GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=5)))]
    
    edges_with_loop = [(GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=1))), 
                       (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=2))), 
                       (GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=0)))]
    
    edges_with_self_loop = [(GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=1))), 
                            (GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=2))), 
                            (GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=2))), 
                            (GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=3)))]
    
    dfs = DFS(edges=edges)
    result = dfs.run(start_node=GraphNode(0))
    print(result)
        
        