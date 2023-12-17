from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_integer_grid
import heapq
from rich import print

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

VAL_MAP = {
    0: Direction.NORTH,
    1: Direction.EAST,
    2: Direction.SOUTH,
    3: Direction.WEST,
}
INV_MAP = {
    Direction.NORTH: 0,
    Direction.EAST: 1,
    Direction.SOUTH: 2,
    Direction.WEST: 3,
}
REV_MAP = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}
DIR_MAP = {
    "NORTH": "^",
    "SOUTH": "v",
    "WEST": "<",
    "EAST": ">",
}

STREAK_LIM = 3
DIRS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

def print_grid(grid: List[List[str]], history) -> None:
    os.system("clear")
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

def lowest_cost_path(grid: List[List[int]]) -> int:
    distances = [[float('inf') for _ in range(len(grid[0]))] for _ in range(len(grid))]
    distances[0][0] = 0
    start_row, start_col = 0, 0
    raw_start_dir = 0
    start_streak = 0
    priority_queue = [(distances[0][0], start_row, start_col, raw_start_dir, start_streak, [[0, 0, Direction.EAST]])]

    while priority_queue:
        cost, r, c, raw_dir, streak, history = heapq.heappop(priority_queue)
        prev = VAL_MAP[raw_dir]
        if cost > distances[r][c]:
            continue

        for dir in DIRS:
            new_r, new_c = r + dir.value[0], c + dir.value[1]
            if new_r < 0 or new_c < 0 or new_r >= len(grid) or new_c >= len(grid[0]):
                continue
            elif cost + grid[new_r][new_c] > distances[new_r][new_c]:
                continue
            # elif dir == prev and streak + 1 > STREAK_LIM:
            #     continue
            # elif REV_MAP[dir] == prev:
            #     continue
            else:
                new_history = history + [[new_r, new_c, dir]]
                print_grid(grid, new_history)
                distances[new_r][new_c] = cost + grid[new_r][new_c]
                heapq.heappush(priority_queue, (distances[new_r][new_c], new_r, new_c, INV_MAP[dir], get_streak(streak, prev, dir), new_history))

    for row in distances:
        print(row)
    return distances[-1][-1]


def get_lowest_cost_path() -> int:
    grid = parse_integer_grid("2023/day17/input.txt")
    return lowest_cost_path(grid)
    
print(get_lowest_cost_path())
