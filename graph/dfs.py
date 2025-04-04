from typing import List, Set, Dict
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
    
    def find_path(self, start_node: GraphNode, target_node: GraphNode):
        
        graph = self.graph
        visited_set: Set[GraphNode] = set()
        reversed_path: Dict[GraphNode] = {}
        
        def dfs_find_path(at: GraphNode):
            if at in visited_set:
                return False
            
            visited_set.add(at)
            
            if at == target_node:
                return True
            
            for next_node in graph.get(at, []):
                if next_node not in visited_set:
                    reversed_path[next_node] = at 
                    if dfs_find_path(next_node): return True 

            return False
        
        if not dfs_find_path(at=start_node):
            return None
        
        path = []
        node = target_node
        while node in reversed_path:
            path.append(node)
            node = reversed_path[node]  # כאן הייתה השגיאה!

        path.append(start_node)  # להוסיף את הצומת ההתחלתי
        return path[::-1]
    

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
    start_node = GraphNode(value=0)
    result = dfs.run(start_node=start_node)
    print(result)
    
    target_node = GraphNode(value=5)
    path = dfs.find_path(start_node=start_node, target_node=target_node)
    print(f"From node: {start_node.value} to {target_node.value}: "
          f"{' -> '.join(str(node.value) for node in path)}")
        
        