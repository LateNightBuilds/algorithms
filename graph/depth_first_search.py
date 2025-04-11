from typing import Set

import networkx as nx


class DepthFirstSearch:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = set(graph.nodes())

    def run(self, start_node) -> bool:
        if start_node not in self.graph:
            return False

        visited_set: Set = set()

        def dfs(at):
            if at in visited_set:
                return False

            visited_set.add(at)

            for next_node in self.graph.neighbors(at):
                if next_node not in visited_set:
                    dfs(next_node)

            return True

        dfs(start_node)
        return len(visited_set) == len(self.nodes)
