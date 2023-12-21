from typing import List
from lib.parse import parse_string_grid
import numpy as np

DIRS = [[-1,0], [1,0], [0,-1], [0,1]]
EMPTY = {".", "S"}

def print_grid(grid: List[List[str]], targets: List) -> None:
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if (r,c) in targets:
                row += "O"
            else:
                row += grid[r][c]
        print(row)
    print()

def get_possibilities(steps: int) -> int:
    grid = parse_string_grid("2023/day21/input.txt")
    queue = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                queue.add((r,c))
                break
    
    for _ in range(steps):
        next_queue = set()
        for row, col in queue:
            for x,y in DIRS:
                r, c = row+x, col+y
                if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] not in EMPTY:
                    continue
                else:
                    next_queue.add((r,c))
        queue = next_queue
    
    return len(queue)

def get_infinite_possibilities(steps: int) -> int:
    grid = parse_string_grid("2023/day21/input.txt")
    queue = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                queue.add((r,c))
                break

    for _ in range(steps):
        next_queue = set()
        for row, col in queue:
            for x,y in DIRS:
                r, c = row+x, col+y
                if grid[r % len(grid)][c % len(grid[0])] not in EMPTY:
                    continue
                else:
                    next_queue.add((r,c))
        queue = next_queue

    return len(queue)

def compute(x: int) -> int:
    def poly(x, a, b, c):
        return a * x**2 + b * x + c

    x_data = np.array([65, 196, 327])
    y_data = np.array([get_infinite_possibilities(65), get_infinite_possibilities(196), get_infinite_possibilities(327)])

    # Fit a quadratic polynomial (ax^2 + bx + c) to the data
    coefficients = np.polyfit(x_data, y_data, 2)
    a, b, c = coefficients
    return round(poly(x, a, b, c))

# print(get_possibilities(steps=64))
# print(get_infinite_possibilities(steps=500))
print(compute(x=1000))