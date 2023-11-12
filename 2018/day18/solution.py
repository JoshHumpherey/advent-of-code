import os
import time
from typing import Dict, List
from lib.parse import parse_string_grid, parse_strings
from lib.pretty_print import print_grid
from lib.initialize import create_grid

EMPTY = "."
TREE = "|"
LUMBERYARD = "#"
SIM_TIME = 0.1

def get_adjacent_values(grid, row, col) -> Dict[str, str]:
    adjacent_values = {
        EMPTY: 0,
        TREE: 0,
        LUMBERYARD: 0,
    }
    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
    for i, j in directions:
        new_row, new_col = row + i, col + j
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            if grid[new_row][new_col] != " ":
                adjacent_values[grid[new_row][new_col]] += 1
    return adjacent_values

def get_count(grid: List[List[str]], target: str) -> int:
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == target:
                count += 1
    return count

def hash_board(grid: List[List[str]]) -> str:
    hash = ""
    for row in grid:
        hash += "".join(row)
    return hash

def advance_grid(grid: List[List[str]]) -> List[List[str]]:
    next_grid = create_grid(rows=len(grid), cols=len(grid[0]), placeholder=".")
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            adj = get_adjacent_values(grid, r, c)
            if grid[r][c] == EMPTY and adj[TREE] >= 3:
                next_grid[r][c] = TREE
            elif grid[r][c] == TREE and adj[LUMBERYARD] >= 3:
                next_grid[r][c] = LUMBERYARD
            elif grid[r][c] == LUMBERYARD:
                if adj[LUMBERYARD] >= 1 and adj[TREE] >= 1:
                    next_grid[r][c] = LUMBERYARD
                else:
                    next_grid[r][c] = EMPTY
            else:
                next_grid[r][c] = grid[r][c]
    return next_grid
            

def part_1() -> int:
    grid = parse_string_grid("2018/day18/input.txt")
    print_grid(grid)
    for _ in range(10):
        grid = advance_grid(grid)
        os.system("clear")
        print_grid(grid)
        time.sleep(SIM_TIME)

    return get_count(grid, TREE) * get_count(grid, LUMBERYARD)    

def part_2() -> int:
    iterations = 1_000_000_000
    grid = parse_string_grid("2018/day18/input.txt")
    seen = {
        hash_board(grid): 0
    }

    for i in range(1, iterations+1):
        grid = advance_grid(grid)
        hash = hash_board(grid)
        if hash in seen:
            break
        else:
            seen[hash] = i
    
    for key, val in seen.items():
        if val == 440:
            return key.count(TREE) * key.count(LUMBERYARD)

    return -1

print(part_2())