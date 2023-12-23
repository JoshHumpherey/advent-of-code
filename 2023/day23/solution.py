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

def can_move(grid: List[List[str]], r: int, c: int, dir: Direction, history: set) -> None:
    rr, cc = r + dir.value[0], c + dir.value[1]
    if rr < 0 or cc < 0 or rr >= len(grid) or cc >= len(grid[0]) or (rr,cc) in history or grid[rr][cc] == "#":
        return False
    elif grid[r][c] in VALID_MOVE.keys():
        return dir == VALID_MOVE[grid[r][c]]
    elif grid[rr][cc] in VALID_MOVE.keys():
        return dir == VALID_MOVE[grid[rr][cc]]
    else:
        return True

def find_longest_path() -> None:
    grid = parse_string_grid("2023/day23/input.txt")
    queue = [(0, 1, 0, set())]
    best = 0

    while queue:
        next_queue = []
        for r, c, dist, hist in queue:
            best = max(dist, best)
            hist.add((r,c))
            for d in DIRS:
                x,y = r + d.value[0], c + d.value[1]
                if can_move(grid, r, c, d, hist):
                    next_queue.append((x, y, dist+1, set(hist)))
        
        queue = next_queue
    
    return best


print(find_longest_path())
