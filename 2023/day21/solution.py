import time
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

def get_steps_to_reach_target(target: int) -> int:
    grid = parse_string_grid("2023/day21/input.txt")
    queue = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                queue.add((r,c))
                break
    cycles = 0

    while True:
        cycles += 1
        if cycles % 100 == 0:
            print(f"Cycle: {cycles} - queue: {len(queue)}")
        next_queue = set()
        for row, col in queue:
            for x,y in DIRS:
                r, c = row+x, col+y
                if grid[r % len(grid)][c % len(grid[0])] not in EMPTY:
                    continue
                else:
                    next_queue.add((r,c))
        if len(next_queue) == target:
            return cycles
        elif len(next_queue) > target:
            print_grid(grid, next_queue)
            raise Exception(f"Overshot target: {len(next_queue)} in {cycles} cycles")
        queue = next_queue

print(get_possibilities(steps=64))
# assert get_steps_to_reach_target(target=16) == 6
# assert get_steps_to_reach_target(target=50) == 10
# assert get_steps_to_reach_target(target=6536) == 100
# assert get_steps_to_reach_target(target=167004) == 500
# assert get_steps_to_reach_target(target=668697) == 1000
print(get_steps_to_reach_target(target=26501365))