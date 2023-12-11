from typing import List
from lib.parse import parse_string_grid

def get_expanded_grid() -> List[List[str]]:
    grid = parse_string_grid("2023/day11/input.txt")
    empty_rows = set()
    for r in range(len(grid)):
        seen = False
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                seen = True
                break
        if not seen:
            empty_rows.add(r)
    
    empty_cols = set()
    for c in range(len(grid[0])):
        seen = False
        for r in range(len(grid)):
            if grid[r][c] == "#":
                seen = True
                break
        if not seen:
            empty_cols.add(c)

    temp_grid = []
    for r in range(len(grid)):
        if r in empty_rows:
            temp_grid.append(["." for _ in range(len(grid[0]))])
        temp_grid.append(grid[r])
    grid = temp_grid
    
    temp_grid = [[] for _ in range(len(grid))]
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if c in empty_cols:
                temp_grid[r].append(".")
            temp_grid[r].append(grid[r][c])

    grid = temp_grid
    return grid

print(get_expanded_grid())
