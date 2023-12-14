from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_string_grid

SIM_TIME = 0.1

STONE = "O"
BLOCK = "#"
EMPTY = "."

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

def print_grid(grid: List[List[str]], debug: bool = False) -> None:
    if not debug:
        return
    # os.system("clear")
    for row in grid:
        print(''.join(row))
    print()
    time.sleep(SIM_TIME)

def cache_key(grid: List[List[str]]) -> str:
    key = ""
    for row in grid:
        key += ''.join(row)
    return key

def slide_rocks(grid: List[List[str]], dir: Direction) -> bool:
    prev = []
    updated_moves = []
    stationary = []
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == STONE:
                prev.append([r,c])
                rr, cc = r + dir.value[0], c + dir.value[1]
                if rr >= 0 and cc >= 0 and rr < len(grid) and cc < len(grid[0]) and grid[rr][cc] == EMPTY:
                    updated_moves.append([rr, cc])
                else:
                    stationary.append([r, c])
    
    if len(updated_moves) == 0:
        return True
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if [r,c] in prev:
                grid[r][c] = EMPTY
            if [r,c] in updated_moves or [r,c] in stationary:
                grid[r][c] = STONE
    return False
            
def resolve_slide(grid: List[List[str]], dir: Direction) -> None:
    while True:
        if slide_rocks(grid, dir):
            return
        print_grid(grid)

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
    idx = 0
    full_cycle = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]

    while idx < len(full_cycle):
        if slide_rocks(grid, full_cycle[idx]):
            idx += 1
        print_grid(grid)

def get_north_load() -> int:
    grid = parse_string_grid("2023/day14/input.txt")
    resolve_slide(grid, Direction.NORTH)
    print_grid(grid)
    return calculate_load(grid)

def get_spin_cycle_load() -> int:
    grid = parse_string_grid("2023/day14/input.txt")
    cache = {}
    diff = 0

    for i in range(1_000_000_000):
        resolve_spin_cycle(grid)
        key = cache_key(grid)
        if key in cache:
            print(f"DETECTED CYCLE: from {i} to {cache[key]}")
            diff = i - cache[key]
            break
        else:
            cache[key] = i
    
    to_adv = 1_000_000_000 % (diff + i + 1)
    print(diff)
    for _ in range(to_adv):
        print(calculate_load(grid))
        print_grid(grid, debug=True)
        resolve_spin_cycle(grid)

    return calculate_load(grid)

print(get_spin_cycle_load())
