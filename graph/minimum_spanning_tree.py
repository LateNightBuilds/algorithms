import heapq

import networkx as nx

from graph.utils import graph_to_edge_list


class MinimumSpanningTree:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = list(graph.nodes())

    def __post_init__(self):
        if not nx.is_connected(self.graph):
            raise ValueError("Cannot compute MST: the input graph is not connected.")

    def run(self):
        connected_nodes = set()

        edges = graph_to_edge_list(graph=self.graph)
        heapq.heapify(edges)

        mst_edges = []

        while len(connected_nodes) < len(self.nodes) and edges:
            weight, from_node, to_node = heapq.heappop(edges)

            is_nodes_already_connected = (from_node in connected_nodes and
                                          to_node in connected_nodes)

            if is_nodes_already_connected:
                continue

            mst_edges.append((from_node, to_node, weight))
            connected_nodes.update([from_node, to_node])

        if len(connected_nodes) < len(self.nodes):
            raise ValueError("Could not construct complete MST")

        return mst_edges
