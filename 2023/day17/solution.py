from enum import Enum
from typing import List
from lib.parse import parse_integer_grid
import heapq

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

    def __lt__(self, other):
        return self.value < other.value

def get_streak(streak: int, old: Direction, new: Direction) -> int:
    if old == new:
        return streak + 1
    return 1

def get_next_dirs(current_dir: Direction):
    if current_dir == Direction.NORTH:
        return [Direction.WEST, Direction.NORTH, Direction.EAST]
    elif current_dir == Direction.EAST:
        return [Direction.NORTH, Direction.EAST, Direction.SOUTH]
    elif current_dir == Direction.SOUTH:
        return [Direction.WEST, Direction.SOUTH, Direction.EAST]
    else:    
        return [Direction.NORTH, Direction.WEST, Direction.SOUTH]

def lowest_cost_path(grid: List[List[int]]) -> int:
    queue = [(0, 0, 0, Direction.EAST, 0)]
    seen = set()

    while queue:
        curr_cost, r, c, prev_dir, streak = heapq.heappop(queue)
        if r == len(grid)-1 and c == len(grid[0])-1:
            return curr_cost
        elif (r,c,prev_dir,streak) in seen:
            continue

        seen.add((r,c,prev_dir,streak))
        for next_dir in get_next_dirs(current_dir=prev_dir):
            row, col = r + next_dir.value[0], c + next_dir.value[1]
            if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
                continue
            elif prev_dir == next_dir and streak >= 3:
                continue
            else:
                heapq.heappush(queue, ([curr_cost + grid[row][col], row, col, next_dir, get_streak(streak, prev_dir, next_dir)]))
    
    return -1

def lowest_cost_path_ultra(grid: List[List[int]]) -> int:
    queue = [(0, 0, 0, Direction.EAST, 0, [])]
    seen = set()

    while queue:
        curr_cost, r, c, prev_dir, streak, history = heapq.heappop(queue)
        if r == len(grid)-1 and c == len(grid[0])-1:
            if streak >= 4:
                return curr_cost
            else:
                continue
        elif (r,c,prev_dir,streak) in seen:
            continue

        seen.add((r,c,prev_dir,streak))
        if streak < 4:
            row, col = r + prev_dir.value[0], c + prev_dir.value[1]
            if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
                continue
            else:
                heapq.heappush(queue, ([curr_cost + grid[row][col], row, col, prev_dir, streak+1, history + [[row,col]]]))
        elif streak >= 4 and streak <= 10:
            for next_dir in get_next_dirs(current_dir=prev_dir):
                row, col = r + next_dir.value[0], c + next_dir.value[1]
                if next_dir == prev_dir and streak == 10:
                    continue
                elif row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
                    continue
                else:
                    heapq.heappush(queue, ([curr_cost + grid[row][col], row, col, next_dir, get_streak(streak, prev_dir, next_dir), history + [[row,col]]]))
            
    return -1

def get_lowest_cost_path() -> int:
    grid = parse_integer_grid("2023/day17/input.txt")
    return lowest_cost_path(grid)

def get_lowest_cost_path_ultra() -> int:
    grid = parse_integer_grid("2023/day17/input.txt")
    return lowest_cost_path_ultra(grid)
    
print(get_lowest_cost_path())
print(get_lowest_cost_path_ultra())