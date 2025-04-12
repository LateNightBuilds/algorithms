from collections import deque
from typing import Set, Tuple

import networkx as nx
from algorithms.graph.utils.history import HistoryLogger


class BreadthFirstSearch:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = set(graph.nodes())
        self.history = HistoryLogger()

    def run(self, start_node) -> Tuple[bool, HistoryLogger]:
        if start_node not in self.graph:
            return False, self.history

        queue = deque([start_node])
        visit_set: Set = set()

        while queue:
            node = queue.popleft()
            self.history.add_new_step(node=node)

            if node in visit_set:
                continue

            visit_set.add(node)

            for next_node in self.graph.neighbors(node):
                if next_node not in visit_set:
                    queue.append(next_node)

        return visit_set == self.nodes, self.history
