from typing import List, Tuple
from lib.parse import parse_string_grid

class Space:

    def __init__(self, grid: List[List[str]], empty_rows: set, empty_cols: set, modifier: int) -> None:
        self.grid = grid
        self.empty_rows = empty_rows
        self.empty_cols = empty_cols
        self.modifier = modifier
        self.galaxies = []

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == "#":
                    self.galaxies.append([r,c])

    def dist(self, g1: Tuple[int, int], g2: Tuple[int, int]) -> int:
        dist = abs(g1[1] - g2[1]) + abs(g1[0] - g2[0])
        r_range = sorted([g1[0], g2[0]])
        c_range = sorted([g1[1], g2[1]])

        for r in self.empty_rows:
            if r_range[0] < r and r < r_range[1]:
                dist += self.modifier
        for c in self.empty_cols:
            if c_range[0] < c and c < c_range[1]:
                dist += self.modifier

        return dist


def get_space(modifier: int) -> Space:
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

    return Space(grid=grid, empty_rows=empty_rows, empty_cols=empty_cols, modifier=modifier)
    

def get_total_weights() -> int:
    space = get_space(modifier=1)
    total = 0
    for i in range(0, len(space.galaxies)):
        for j in range(i+1, len(space.galaxies)):
            local = space.dist(space.galaxies[i], space.galaxies[j])
            # print(f"{i+1}->{j+1}: {local}")
            total += local

    return total

print(get_total_weights())
