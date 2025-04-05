from typing import List, Dict, Set
import heapq

from utils import (GraphEdge, GraphNode, 
                   edges_list_to_adjacency_list,
                   edges_list_to_nodes_set,
                   print_edges)
from depth_first_search import DepthFirstSearch

class MinimumSpanningTree:
    def __init__(self, edges: List[GraphEdge]):
        self.edges = edges
        self.nodes: Set[GraphNode] = edges_list_to_nodes_set(edges=self.edges)
        self.adjacency_list: Dict[GraphNode, List[GraphNode]] = (
            edges_list_to_adjacency_list(edges=self.edges))
        
    def __post_init__(self):
        dfs = DepthFirstSearch(edges=self.edges)
        
        any_node = self.nodes[0]
        if not dfs.run(start_node=any_node):
            ValueError("Cannot compute MST: the input graph is not connected.")
        
    def run(self):
        connected_nodes = set()
        heap = [*self.edges]
        heapq.heapify(heap)
        
        mst_edges: List[GraphEdge] = []
        
        while len(connected_nodes) < len(self.nodes):
            chipest_edge: GraphEdge = heapq.heappop(heap)
            is_nodes_already_connected: bool = (chipest_edge.from_node in connected_nodes
                                                and chipest_edge.to_node in connected_nodes)
            if is_nodes_already_connected:
                continue
            
            mst_edges.append(chipest_edge)
            connected_nodes.update([chipest_edge.from_node, chipest_edge.to_node])
        
        return mst_edges
            
            
            
if __name__ == "__main__":
    edges = [
        GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=1), weight=2),  
        GraphEdge(from_node=GraphNode(value=0), to_node=GraphNode(value=3), weight=6),
        GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=2), weight=3),
        GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=3), weight=8),
        GraphEdge(from_node=GraphNode(value=1), to_node=GraphNode(value=4), weight=5),
        GraphEdge(from_node=GraphNode(value=2), to_node=GraphNode(value=4), weight=7),
        GraphEdge(from_node=GraphNode(value=3), to_node=GraphNode(value=4), weight=9)]
    
    mst = MinimumSpanningTree(edges=edges)
    mst_edges = mst.run()
    print_edges(edges=mst_edges)