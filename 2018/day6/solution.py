from typing import List, Tuple
from lib.parse import parse_integer_pairs
from lib.initialize import create_grid
from lib.pretty_print import print_grid

def manhattan_dist(point_1: Tuple[int, int], point_2: Tuple[int, int]) -> int:
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)

def populate_grid_with_closest_point(grid: List[List[str]], pairs: List[Tuple[int, int]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            seen = False
            best = float('inf')
            idx = 0

            for i in range(len(pairs)):
                dist = manhattan_dist(point_1=(r,c), point_2=pairs[i])
                if dist < best:
                    seen = False
                    best = dist
                    idx = i
                elif dist == best:
                    seen = True
            if seen:
                grid[r][c] = "."
            else:
                grid[r][c] = chr(idx+97)

def populate_grid_with_dist_sum(grid: List[List[str]], pairs: List[Tuple[int, int]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            total_dist = 0
            if r % 1_000 == 0 and c == 0:
                print(f"Populated {r}...")
            for i in range(len(pairs)):
                total_dist += manhattan_dist(point_1=(r,c), point_2=pairs[i])
            if total_dist < 10_000:
                grid[r][c] = "#"



def get_area(grid: List[List[str]], row: int, col: int, visited: set, target: str) -> float:
    queue = [(row,col)]

    while queue:
        next_queue = []
        for r, c in queue:
            if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
                return float('inf')
            elif grid[r][c] != target or (r,c) in visited:
                continue
            else:
                visited.add((r,c))
                next_steps = [[1,0], [-1,0], [0,1], [0,-1]]
                for i in range(len(next_steps)):
                    rr, cc = r+next_steps[i][0], c+next_steps[i][1]
                    if ((rr, cc)) not in visited:
                        next_queue.append((rr, cc))
        queue = next_queue

    return len(visited)

def get_area_and_paint(grid: List[List[str]], row: int, col: int) -> int:
    queue = [(row, col)]
    area = 0
    while queue:
        next_queue = []
        for r, c in queue:
            if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
                continue
            elif grid[r][c] != "#":
                continue
            else:
                grid[r][c] = "."
                area += 1
                next_steps = [[1,0], [-1,0], [0,1], [0,-1]]
                for i in range(len(next_steps)):
                    rr, cc = r+next_steps[i][0], c+next_steps[i][1]
                    next_queue.append((rr, cc))
        queue = next_queue
    return area


def get_largest_finite_area() -> int:
    pairs = parse_integer_pairs("2018/day6/input.txt")
    for i in range(len(pairs)):
        pairs[i][0], pairs[i][1] = pairs[i][1], pairs[i][0]  # type: ignore

    grid = create_grid(rows=1000, cols=1000, placeholder=".")
    populate_grid_with_closest_point(grid=grid, pairs=pairs)
    
    best = 0
    for r,c in pairs:
        local = get_area(grid, r, c, set(), grid[r][c])
        if local != float('inf') and local > best:
            best = local

    return int(best)

def get_most_common_area() -> int:
    pairs = parse_integer_pairs("2018/day6/input.txt")
    for i in range(len(pairs)):
        pairs[i][0], pairs[i][1] = pairs[i][1], pairs[i][0]  # type: ignore

    print("Creating Grid...")
    grid = create_grid(rows=11_000, cols=11_000, placeholder=".")
    print("Populating Grid...")
    populate_grid_with_dist_sum(grid=grid, pairs=pairs)
    print("Grid is fully populated")

    best = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                print(f"Examining {[r,c]}")
                local = get_area_and_paint(grid, r, c)
                best = max(local, best)

    return int(best)


print(get_most_common_area())