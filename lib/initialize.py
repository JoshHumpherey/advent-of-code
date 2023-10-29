from typing import Any, List


def create_grid(rows: int, cols: int, placeholder: Any = 0) -> List[List[Any]]:
    """
    Initializes a grid with a given placeholder
    """
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(placeholder)
        grid.append(row)
    return grid
