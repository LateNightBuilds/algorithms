import heapq

import networkx as nx

from algorithms.graph.utils import graph_to_edge_list, HistoryLogger


class PrimAlgorithm:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = list(graph.nodes())
        self.history = HistoryLogger()

    def run(self):
        if not nx.is_connected(self.graph):
            raise ValueError("Cannot compute MST: the input graph is not connected.")

        start_node = self.nodes[0]

        mst_nodes = {start_node}

        mst_edges = []

        available_edges = []

        for neighbor in self.graph.neighbors(start_node):
            weight = self.graph[start_node][neighbor]['weight']
            heapq.heappush(available_edges, (weight, start_node, neighbor))

        while available_edges and len(mst_nodes) < len(self.nodes):
            weight, from_node, to_node = heapq.heappop(available_edges)
            self.history.add_new_step(node=to_node)

            if to_node in mst_nodes:
                continue

            mst_edges.append((from_node, to_node, weight))
            mst_nodes.add(to_node)

            for neighbor in self.graph.neighbors(to_node):
                if neighbor not in mst_nodes:
                    neighbor_weight = self.graph[to_node][neighbor]['weight']
                    heapq.heappush(available_edges, (neighbor_weight, to_node, neighbor))

        if len(mst_nodes) < len(self.nodes):
            raise ValueError("Could not construct complete MST")

        return mst_edges, self.history