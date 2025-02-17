from typing import List
from lib.parse import parse_string_groups
import copy

def print_grid(grid: List[str], row: int, col: int) -> None:
    printed_grid = []

    if row != -1:
        for r in range(len(grid)):
            if r == row:
                printed_grid.append("-" * len(grid[0]))
            printed_grid.append(grid[r])
    elif col != -1:
        for r in range(len(grid)):
            full_row = ""
            for c in range(len(grid[0])):
                if c == col:
                    full_row += "|"
                full_row += grid[r][c]
            printed_grid.append(full_row)
    else:
        printed_grid = grid

    for r in printed_grid:
        print(''.join(r))
    print()

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

def get_reflections(grid: List[List[str]], banned_row: int, banned_col: int) -> List[int]:
    res = [-1, -1]

    for r in range(1, len(grid)):
        if is_horizontal_mirror(grid, r-1, r) and r != banned_row:
            return [r, -1]
    for c in range(1, len(grid[0])):
        if is_vertical_mirror(grid, c-1, c) and c != banned_col:
            return [-1, c]
    
    return res

def reverse(grid: List[List[str]], r: int, c: int) -> List[List[str]]:
    if grid[r][c] == ".":
        grid[r][c] = "#"
    else: # grid[r][c] == "#"
        grid[r][c] = "."

    return grid

def get_error_corrected_reflections(grid: List[List[str]], banned_row: int, banned_col: int) -> List[int]:
    res = [-1, -1]

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            copied_grid = copy.deepcopy(grid)
            copied_grid = reverse(copied_grid, r, c)
            row, col = get_reflections(copied_grid, banned_row, banned_col)
            if row != -1 and row != banned_row:
                res[0] = row
            if col != -1 and col != banned_col:
                res[1] = col
    
    if res == [-1, -1]:
        print(f"Banned: {banned_row, banned_col}")
        print_grid(grid, -1, -1)
    return res

def get_pattern_sums() -> int:
    grids = parse_string_groups("2023/day13/input.txt")
    for g in grids:
        for r in range(len(g)):
            g[r] = list(g[r])

    res = 0
    for g in grids:
        row, col = get_reflections(g, -1, -1)
        if row != -1:
            res += (row * 100)
        if col != -1:
            res += col
    
    return res

def get_corrected_pattern_sums() -> int:
    grids = parse_string_groups("2023/day13/input.txt")
    for g in grids:
        for r in range(len(g)):
            g[r] = list(g[r])
    
    res = 0
    for g in grids:
        banned_row, banned_col = get_reflections(g, -1, -1)
        row, col = get_error_corrected_reflections(g, banned_row, banned_col)
        if row != -1:
            res += (row * 100)
        elif col != -1:
            res += col
    
    return res

print(get_pattern_sums())
print(get_corrected_pattern_sums())