from typing import List


def create_grid(rows: int, cols: int) -> List[List[int]]:
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(0)
        grid.append(row)
    return grid
