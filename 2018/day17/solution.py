from typing import List
from lib.parse import parse_x_y_pairs
from lib.initialize import create_grid
from lib.pretty_print import print_bounded_grid

EMPTY = "."
SETTLED = "~"
FLOWING = "|"
CLAY = "#"
SOURCE = "+"

def initialize_grid() -> List[List[str]]:
    data = parse_x_y_pairs("2018/day17/input.txt")
    coords = []
    max_col = 0
    max_row = 0

    for d in data:
        if ".." in d[0]:
            start, end = d[0].split("..")
            coords.append([[int(start), int(end)], int(d[1])])
            max_row = max(max_row, int(start), int(end))
            max_col = max(max_col, int(d[1]))
        else:
            start, end = d[1].split("..")
            coords.append([int(d[0]), [int(start), int(end)]])
            max_row = max(max_row, int(d[0]))
            max_col = max(max_col, int(start), int(end))

    max_col += 1
    max_row += 1

    grid = create_grid(rows=max_row, cols=max_col, placeholder=EMPTY)
    grid[0][500] = SOURCE

    for v1, v2 in coords:
        if type(v1) == int:
            for c in range(v2[0], v2[1]+1):
                grid[v1][c] = CLAY
        if type(v2) == int:
            for r in range(v1[0], v1[1]+1):
                grid[r][v2] = CLAY
    return grid

def advance_droplet(grid: List[List[str]]) -> List[List[str]]:
    if grid[1][500] == FLOWING:
        return grid
    
    # TODO: Simulate droplet physics






def simulate() -> None:
    grid = initialize_grid()
    print_bounded_grid(grid=grid, interesting=set([SETTLED, FLOWING, CLAY, SOURCE]), placeholder=EMPTY)


simulate()