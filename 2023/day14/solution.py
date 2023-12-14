from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_string_grid

SIM_TIME = 0.5

STONE = "O"
BLOCK = "#"
EMPTY = "."

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

def print_grid(grid: List[List[str]]) -> None:
    os.system("clear")
    for row in grid:
        print(''.join(row))
    print()
    time.sleep(SIM_TIME)

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


def get_north_load() -> int:
    grid = parse_string_grid("2023/day14/input.txt")
    resolve_slide(grid, Direction.NORTH)
    print_grid(grid)
    return calculate_load(grid)

print(get_north_load())
