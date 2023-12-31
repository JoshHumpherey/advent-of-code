from typing import List, Tuple
from lib.parse import parse_string_grid
import math

NON_SYMBOLS = {"0","1","2","3","4","5","6","7","8","9","."," "}

def is_adj(grid: List[List[any]], coords: List[Tuple[int, int]]) -> bool:
    adj = [[-1,-1], [-1,0], [-1,1], [0,-1], [0, 1], [1,-1], [1,0], [1,1]]
    
    for pair in coords:
        for r_offset, c_offset in adj:
            row, col = pair[0] + r_offset, pair[1] + c_offset
            if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or grid[row][col] in NON_SYMBOLS:
                continue
            else:
                return True
    return False

def get_gears(grid: List[List[any]],) -> set:
    gears = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "*":
                gears.add((r,c))
    return gears

def get_numbers(grid: List[List[any]]) -> List[Tuple[int, Tuple[int, int]]]:
    numbers = []
    for r in range(len(grid)):
        num, coords = "", []
        for c in range(len(grid[0])):
            if grid[r][c] in NON_SYMBOLS and grid[r][c] != "." and grid[r][c] != " ":
                num += grid[r][c]
                coords.append([r,c])
            elif len(num) > 0:
                numbers.append([int(num), coords])
                num, coords = "", []

        if len(num) > 0:
            numbers.append([int(num), coords])
            num, coords = "", []
    
    return numbers

def get_part_numbers() -> int:
    grid = parse_string_grid("2023/day3/input.txt")
    numbers = get_numbers(grid)
    res = 0

    for val, coords in numbers:
        if is_adj(grid, coords):
            res += val
    return res

def get_gear_numbers() -> int:
    grid = parse_string_grid("2023/day3/input.txt")
    numbers = get_numbers(grid)
    gears = get_gears(grid)
    res = 0

    for gear_r, gear_c in gears:
        touches = []
        for val, coords in numbers:
            touch = False
            for r,c in coords:
                if abs(gear_r - r) <= 1 and abs(gear_c - c) <= 1:
                    touch = True
            if touch:
                touches.append(val)
        if len(touches) == 2:
            res += math.prod(touches)
    
    return res
        

print(get_part_numbers())
print(get_gear_numbers())