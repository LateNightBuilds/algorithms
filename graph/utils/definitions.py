from enum import StrEnum


class GridCellType(StrEnum):
    START = 'start'
    OPEN_PATH = 'open_path'
    BLOCK = 'block'
    OBSTACLE = 'obstacle'
    END = 'end'
