from typing import List, Tuple
from lib.parse import parse_string_grid

def is_valid(grid: List[List[str]], r: int, c: int) -> bool:
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0])

def get_possible_connections(grid: List[List[str]], r: int, c: int) -> List[Tuple[int, int]]:
    to_eval = []
    if grid[r][c] == "|":
        to_eval = [[r-1,c], [r+1,c]]
    elif grid[r][c] == "-":
        to_eval = [[r,c-1], [r, c+1]]
    elif grid[r][c] == "L":
        to_eval = [[r-1,c], [r,c+1]]
    elif grid[r][c] == "J":
        to_eval = [[r,c-1], [r-1,c]]
    elif grid[r][c] == "7":
        to_eval = [[r,c-1], [r+1,c]]
    elif grid[r][c] == "F":
        to_eval = [[r+1,c], [r,c+1]]
    elif grid[r][c] == "S":
        to_eval = [[r+1,c], [r-1,c], [r,c+1], [r,c-1]]
    
    possible = []
    for row,col in to_eval:
        if is_valid(grid, row, col):
            possible.append([row,col])

    return possible

def get_connections(grid: List[List[str]], row: int, col: int) -> List[Tuple[int, int]]:
    possible_connections = get_possible_connections(grid, row, col)
    connections = []
    for r,c in possible_connections:
        found = get_possible_connections(grid, r, c)
        if [row, col] in found:
            connections.append([r, c])
    
    return connections

def pipe_bfs(grid: List[List[str]], start_row: int, start_col: int) -> int:
    visited = set()
    dist = 0
    queue = [[start_row, start_col]]

    while queue:
        next_queue = []
        for r,c in queue:
            visited.add((r,c))
            connections = get_connections(grid, r, c)
            for rr, cc in connections:
                if is_valid(grid, rr, cc) and (rr, cc) not in visited:
                    next_queue.append([rr, cc])
        
        dist += 1
        queue = next_queue

    return dist-1 if dist > 0 else 0


def farthest_pipe_dist() -> None:
    grid = parse_string_grid("2023/day10/input.txt")
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                return pipe_bfs(grid, r, c)
    
    return -1
    
print(farthest_pipe_dist())
