from enum import Enum
from typing import List
from lib.parse import parse_string_grid

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT  = (0, 1)

DIRS = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
VALID_MOVE = {
    ">": Direction.RIGHT,
    "<": Direction.LEFT,
    "^": Direction.UP,
    "v": Direction.DOWN,
}

def can_move(grid: List[List[str]], r: int, c: int, dir: Direction, history: set, ignore_peaks: bool) -> None:
    rr, cc = r + dir.value[0], c + dir.value[1]
    if rr < 0 or cc < 0 or rr >= len(grid) or cc >= len(grid[0]) or (rr,cc) in history or grid[rr][cc] == "#":
        return False
    elif not ignore_peaks:
        if grid[r][c] in VALID_MOVE.keys():
            return dir == VALID_MOVE[grid[r][c]]
        if grid[rr][cc] in VALID_MOVE.keys():
            return dir == VALID_MOVE[grid[rr][cc]]
    return True

def find_longest_path(ignore_peaks: bool = False) -> None:
    grid = parse_string_grid("2023/day23/input.txt")
    queue = [(0, 1, 0, set())]
    best = 0

    while queue:
        print(f"Queue: {len(queue)}")
        next_queue = []
        for r, c, dist, hist in queue:
            if r == len(grid)-1 and c == len(grid[0])-2:
                best = max(best, dist)
                continue

            hist.add((r,c))
            for d in DIRS:
                x,y = r + d.value[0], c + d.value[1]
                if can_move(grid, r, c, d, hist, ignore_peaks):
                    next_queue.append((x, y, dist+1, set(hist)))
        
        queue = next_queue
    
    return best


print(find_longest_path(ignore_peaks=True))
