import os
from typing import List, Tuple
from lib.parse import parse_integers
from lib.initialize import create_grid

def get_rack_id(x: int) -> int:
    return x + 10

def get_power_level(x: int, y: int, serial_num: int) -> int:
    rack_id = get_rack_id(x=x)
    power_level = rack_id * y
    power_level += serial_num
    power_level *= rack_id
    raw_power = str(power_level)
    hundreds_digit = 0
    if len(raw_power) >= 3:
        hundreds_digit = int(raw_power[len(raw_power)-3])
    return hundreds_digit - 5

def create_power_grid() -> List[List[int]]:
    serial_num = parse_integers("2018/day11/input.txt")[0]
    grid = create_grid(rows=301, cols=301, placeholder=0)
    for y in range(1, len(grid)):
        for x in range(1, len(grid[0])):
            grid[y][x] = get_power_level(x=x, y=y, serial_num=serial_num)

    return grid

def get_box_sum(x_start: int, y_start: int, grid: List[List[int]], size: int) -> int:
    area = 0
    for y in range(y_start, y_start+size):
        for x in range(x_start, x_start+size):
            if 1 <= y <= len(grid)-1 and 1 <= x <= len(grid[0])-1:
                area += grid[y][x]
    return area

def get_largest_area() -> Tuple[int, int, int]:
    grid = create_power_grid()
    best_pair = (-1, -1, -1)
    best_area = 0

    for y in range(1, len(grid)):
        for x in range(1, len(grid[0])):
            os.system("clear")
            print(f"Evaluating {x,y}")
            x_lim = len(grid[0])-x
            y_lim = len(grid)-y
            lim = min(x_lim, y_lim)
            for size in range(1, lim):
                area = get_box_sum(x_start=x, y_start=y, grid=grid, size=size)
                if area > best_area:
                    best_area = area
                    best_pair = (x, y, size)

    return best_pair

print(get_largest_area())