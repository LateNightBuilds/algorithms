from dataclasses import dataclass


@dataclass(frozen=True)
class GraphNode:
    value: int
    
    
@dataclass(frozen=True)
class GraphEdge:
    from_node: GraphNode
    to_node: GraphNode