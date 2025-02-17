from typing import List
from lib.parse import parse_string_grid

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

    res = []
    for _ in range(steps):
        res.append(len(queue))
        next_queue = set()
        for row, col in queue:
            for x,y in DIRS:
                r, c = row+x, col+y
                if grid[r % len(grid)][c % len(grid[0])] not in EMPTY:
                    continue
                else:
                    next_queue.add((r,c))
        queue = next_queue

    return res[len(res)-2]

def compute_poly(x: int) -> int:
    grid = parse_string_grid("2023/day21/input.txt")
    # polynomials were computed manually by hand via wolframalpha
    a = 3703
    b = 32712
    c = 90559
    n = x // len(grid)
    return a+n*(b-a+(n-1)*(c-b-b+a)//2)

print(get_possibilities(steps=64))
print(compute_poly(x=26501365))