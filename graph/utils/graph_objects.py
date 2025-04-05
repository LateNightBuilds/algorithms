from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class GraphNode:
    value: int
    
    
@dataclass(frozen=True)
class GraphEdge:
    from_node: GraphNode
    to_node: GraphNode
    weight: float = 1.0 
    
    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight >= other.weight
    
def print_edges(edges: List[GraphEdge]):
    for edge in edges:
        print(f"From node: {edge.from_node.value}, To node: {edge.to_node.value}, Weight: {edge.weight}")
        
def print_nodes(nodes: List[GraphNode]):
    print(f"{' -> '.join(str(node.value) for node in nodes)}")