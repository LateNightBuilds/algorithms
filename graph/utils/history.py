from typing import Any


class HistoryLogger:
    def __init__(self):
        self.step = 0
        self.history_dict = {}

    def add_new_step(self, node: Any, data: Any | None = None):
        self.history_dict[self.step] = (node, data) if data else node
        self.step += 1
