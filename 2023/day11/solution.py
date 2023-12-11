from typing import List
from lib.parse import parse_string_grid

def get_expanded_grid() -> List[List[str]]:
    grid = parse_string_grid("2023/day11/input.txt")
    empty_rows = set()
    for r in range(len(grid)):
        seen = False
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                seen = True
                break
        if not seen:
            empty_rows.add(r)
    
    empty_cols = set()
    for c in range(len(grid[0])):
        seen = False
        for r in range(len(grid)):
            if grid[r][c] == "#":
                seen = True
                break
        if not seen:
            empty_cols.add(c)

    temp_grid = []
    for r in range(len(grid)):
        if r in empty_rows:
            temp_grid.append(["." for _ in range(len(grid[0]))])
        temp_grid.append(grid[r])
    grid = temp_grid
    
    temp_grid = [[] for _ in range(len(grid))]
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if c in empty_cols:
                temp_grid[r].append(".")
            temp_grid[r].append(grid[r][c])

    grid = temp_grid
    return grid


def get_galaxy_map(grid: List[List[str]]) -> dict:
    galaxies = {}
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                galaxies[(r,c)] = str(count)
                count += 1

    return galaxies

def get_neighboring_galaxies(grid: List[List[str]], galaxies: dict, start_row: int, start_col: int) -> list:
    queue = [[start_row, start_col]]
    res = []
    visited = set()
    dist = 0

    while queue:
        next_queue = []
        for r, c in queue:
            if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or (r,c) in visited:
                continue
            elif (r,c) in galaxies and (r,c) != (start_row, start_col):
                res.append([r, c, dist])
            
            visited.add((r,c))
            next_queue.append([r-1, c])
            next_queue.append([r+1, c])
            next_queue.append([r, c-1])
            next_queue.append([r, c+1])
        
        dist += 1
        queue = next_queue
    
    return res


def get_weighted_galaxy_graph(grid: List[List[str]], galaxies: dict) -> dict:
    galaxy_weights = {}

    for loc, galaxy in galaxies.items():
        galaxy_weights[galaxy] = get_neighboring_galaxies(grid, galaxies, loc[0], loc[1])

    return galaxy_weights
    grid = get_expanded_grid()
    galaxies = get_galaxy_map(grid)
    galaxy_weights = get_weighted_galaxy_graph(grid, galaxies)

    visited = [0]*len(galaxies.keys())
    row,col = next(iter(galaxies.keys()))
    total = 0

    while sum(visited) != len(visited):
        g = galaxies[(row,col)]
        visited[int(g)] = 1
        next_row, next_col, best = -1, -1, float('inf')
        for r,c,d in galaxy_weights[g]:
            new_g = galaxies[(r,c)]
            if visited[int(new_g)] == 0 and d < best:
                best = d
                next_row, next_col = r, c

        row, col = next_row, next_col
        if row == -1 and col == -1:
            return total
        else:
            total += best

    return total 

def get_total_weights() -> int:
    grid = get_expanded_grid()
    galaxies = get_galaxy_map(grid)
    galaxy_weights = get_weighted_galaxy_graph(grid, galaxies)

    total = 0
    added = set()

    for source_galaxy, dists in galaxy_weights.items():
        for r,c,d in dists:
            dest_galaxy = galaxies[(r,c)]
            if str(source_galaxy + dest_galaxy) not in added:
                total += d
            added.add(str(source_galaxy + dest_galaxy))
            added.add(str(dest_galaxy + source_galaxy))
    
    return total

print(get_total_weights())
