from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_string_grid

SIM_TIME = 0.05
DEBUG = False

STONE = "O"
BLOCK = "#"
EMPTY = "."

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

def print_grid(grid: List[List[str]]) -> None:
    if not DEBUG:
        return
    os.system("clear")
    for row in grid:
        print(''.join(row))
    print()
    time.sleep(SIM_TIME)

def cache_key(grid: List[List[str]]) -> str:
    key = ""
    for row in grid:
        key += ''.join(row)
    return key

def slide_stones(grid: List[List[str]], dir: Direction, stones: List) -> None:
    while True:
        moved = False
        next_stones = []
        for r, c in stones:
            rr, cc = r + dir.value[0], c + dir.value[1]
            if rr >= 0 and cc >= 0 and rr < len(grid) and cc < len(grid[0]) and grid[rr][cc] == EMPTY:
                grid[r][c] = EMPTY
                grid[rr][cc] = STONE
                moved = True
                next_stones.append([rr, cc])
            else:
                next_stones.append([r, c])

        print_grid(grid)
        stones = next_stones
        if not moved:
            return

            
def resolve_slide(grid: List[List[str]], dir: Direction) -> None:
    stones = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == STONE:
                stones.append([r,c])

    slide_stones(grid, dir, stones)
    return

def calculate_load(grid: List[List[str]]) -> int:
    factor = len(grid)
    res = 0

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == STONE:
                res += factor
        factor -= 1
    
    return res

def resolve_spin_cycle(grid: List[List[str]]) -> None:
    for dir in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
        resolve_slide(grid, dir)
    return

def get_north_load() -> int:
    grid = parse_string_grid("2023/day14/input.txt")
    resolve_slide(grid, Direction.NORTH)
    print_grid(grid)
    return calculate_load(grid)

def get_spin_cycle_load() -> int:
    grid = parse_string_grid("2023/day14/input.txt")
    cache = {cache_key(grid): [0, calculate_load(grid)]}
    cycle_start = -1
    cycle_len = -1

    for i in range(1, 1_000+1):
        resolve_spin_cycle(grid)
        key = cache_key(grid)
        if key in cache:
            cycle_start = cache[key][0]
            cycle_len = i - cycle_start
            break
        else:
            cache[key] = [i, calculate_load(grid)]

    target = ((1_000_000_000 - cycle_start) % cycle_len) + cycle_start
    print(f"Cycle Info: start={cycle_start}, len={cycle_len}, target={target}")
    
    for idx, load in cache.values():
        if idx == target:
            return load
    
    return -1

print(get_north_load())
print(get_spin_cycle_load())
