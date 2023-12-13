from typing import List, Tuple
from lib.parse import parse_string_groups
from collections import defaultdict

def is_horizontal_mirror(grid: List[List[str]], left: int, right: int) -> bool:
    while left >= 0 and right < len(grid):
        if grid[left][:] == grid[right][:]:
            left -= 1
            right += 1
        else:
            return False
    
    return True

def is_vertical_mirror(grid: List[List[str]], left: int, right: int) -> bool:
    while left >= 0 and right < len(grid[0]):
        left_col = [row[left] for row in grid]
        right_col = [row[right] for row in grid]
        if left_col == right_col:
            left -= 1
            right += 1
        else:
            return False

    return True

def get_reflections(grid: List[List[str]]) -> List[int]:
    res = [-1, -1]

    for r in range(1, len(grid)):
        if is_horizontal_mirror(grid, r-1, r):
            res[0] = r
    for c in range(1, len(grid[0])):
        if is_vertical_mirror(grid, c-1, c):
            res[1] = c
    
    return res
        

def get_pattern_sums() -> None:
    grids = parse_string_groups("2023/day13/input.txt")
    res = 0

    for g in grids:
        row, col = get_reflections(g)
        if row != -1:
            res += (row * 100)
        if col != -1:
            res += col
    
    return res

print(get_pattern_sums())
