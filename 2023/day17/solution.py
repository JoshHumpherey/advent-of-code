from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_integer_grid
import heapq
from copy import deepcopy
from rich import print

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

    def __lt__(self, other):
        return self.value < other.value

DIR_MAP = {
    "NORTH": "^",
    "SOUTH": "v",
    "WEST": "<",
    "EAST": ">",
}
STREAK_LIM = 3

def print_grid(grid: List[List[str]], history) -> None:
    for r in range(len(grid)):
        pretty = "[white]"
        for c in range(len(grid[0])):
            match = False
            d = "@"
            for rr, cc, dir in history:
                if [r,c] == [rr, cc]:
                    match = True
                    d = dir
                    break
            if match:
                pretty += f"[red]{DIR_MAP[dir.name]}[/red]"
            else:
                pretty += str(grid[r][c])

        pretty += "[/white]"
        print(pretty)
    print()

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
            elif prev_dir == next_dir and streak >= STREAK_LIM:
                continue
            else:
                heapq.heappush(queue, ([curr_cost + grid[row][col], row, col, next_dir, get_streak(streak, prev_dir, next_dir)]))
    
    return -1


def get_lowest_cost_path() -> int:
    grid = parse_integer_grid("2023/day17/input.txt")
    return lowest_cost_path(grid)
    
print(get_lowest_cost_path())