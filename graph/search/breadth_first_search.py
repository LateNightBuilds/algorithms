from collections import deque
from typing import Set

import networkx as nx


class BreadthFirstSearch:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = set(graph.nodes())

    def run(self, start_node) -> bool:
        if start_node not in self.graph:
            return False

        queue = deque([start_node])
        visit_set: Set = set()

        while queue:
            node = queue.popleft()
            if node in visit_set:
                continue

            visit_set.add(node)

            for next_node in self.graph.neighbors(node):
                if next_node not in visit_set:
                    queue.append(next_node)

        return visit_set == self.nodes
