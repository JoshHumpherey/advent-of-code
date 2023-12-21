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

print(get_possibilities(steps=64))
