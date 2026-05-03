from typing import List

class Grid:

    def __init__(self, nums: List[List[int]]):
        self.grid = nums

    def is_low_value(self, r: int, c: int) -> bool:
        up = self.get_val(r-1, c)
        down = self.get_val(r+1, c)
        left = self.get_val(r, c-1)
        right = self.get_val(r, c+1)
        val = self.get_val(r, c)
        return val < up and val < down and val < left and val < right

    def get_val(self, r: int, c: int) -> int:
        if r < 0 or c < 0 or r >= len(self.grid) or c >= len(self.grid[0]):
            return float('inf')
        return self.grid[r][c]

def get_grid() -> Grid:
    with open('input.txt') as f:
        lines = f.readlines()
        grid = []
        for l in lines:
            row = []
            for val in l:
                if val != '\n':
                    row.append(int(val))
            grid.append(row)
        return Grid(nums=grid)

def get_low_value_sum(grid: Grid) -> int:
    risk_value = 0
    for r in range(len(grid.grid)):
        for c in range(len(grid.grid[0])):
            if grid.is_low_value(r, c):
                risk_value += (grid.get_val(r,c) + 1)
    
    return risk_value

def get_basin_size(grid: Grid, row: int, col: int) -> int:
    queue = [(row,col,float('-inf'))]
    visited = set()

    while queue:
        next_queue = []
        for r,c,p in queue:
            if (r,c) in visited or grid.get_val(r,c) <= p:
                continue
            else:
                visited.add((r,c))
                dirs = [[0,1], [0,-1], [1,0], [-1,0]]
                for r_offset,c_offset in dirs:
                    rr, cc = r + r_offset, c + c_offset
                    if (rr,cc) not in visited and rr >= 0 and cc >= 0 and rr < len(grid.grid) and cc < len(grid.grid[0]) and grid.get_val(rr,cc) != 9:
                        next_queue.append((rr, cc, grid.get_val(r,c)))
        queue = next_queue

    return len(visited)

def get_largest_basin_sizes(grid: Grid) -> int:
    basins = []
    for r in range(len(grid.grid)):
        for c in range(len(grid.grid[0])):
            if grid.is_low_value(r,c):
                basin_size = get_basin_size(grid, r, c)
                basins.append(basin_size)
    
    basins = sorted(basins)
    n = len(basins)
    return basins[n-1] * basins[n-2] * basins[n-3]





p1 = get_low_value_sum(get_grid())
print(p1)

p2 = get_largest_basin_sizes(get_grid())
print(p2)