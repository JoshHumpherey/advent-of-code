class Grid:

    def __init__(self, numbers):
        self.grid = [ [0]*len(numbers[0]) for _ in range(len(numbers)) ]
        for r in range(0, len(numbers)):
            for c in range(0, len(numbers[0])):
                self.grid[r][c] = numbers[r][c]

    def is_low(self, row, col) -> bool:
        candidate = self.get_val(row, col)
        p1 = self.get_val(row+1, col)
        p2 = self.get_val(row-1, col)
        p3 = self.get_val(row, col+1)
        p4 = self.get_val(row, col-1)

        if candidate < p1 and candidate < p2 and candidate < p3 and candidate < p4:
            return True
        return False
        
    def get_val(self, row, col) -> int:
        if row >= len(self.grid) or row < 0 or col >= len(self.grid[0]) or col < 0:
            return 99999
        else:
            return self.grid[row][col]

    
    
    def basin(self, row, col) -> int:
        size = 0
        queue = [(row, col, self.grid[row][col])]
        visited = set()
        
        while queue:
            next_queue = []
            for r,c,last in queue:
                if ((r,c) in visited
                    or r < 0 
                    or r >= len(self.grid)
                    or c < 0 or c >= len(self.grid[0])
                    or self.grid[r][c] == 9
                    or (self.grid[r][c] <= last and [row, col] != [r,c])
                   ):
                    continue
                else:
                    size += 1
                    visited.add((r,c))
                    next_queue.append((r+1, c, self.grid[r][c]))
                    next_queue.append((r-1, c, self.grid[r][c]))
                    next_queue.append((r, c+1, self.grid[r][c]))
                    next_queue.append((r, c-1, self.grid[r][c]))
            queue = next_queue
        return size
    
    def print(self):
        for row in self.grid:
            print(row)

def get_grid() -> Grid:
    with open('day9/input.txt') as f:
        lines = f.readlines()
        data = []
        for l in lines:
            row = []
            numstrs = l.strip()
            for s in numstrs:
                row.append(int(s.strip()))
            data.append(row)
        return Grid(numbers=data)

def part1() -> int:
    g = get_grid()
    total = 0
    
    for r in range(len(g.grid)):
        for c in range(len(g.grid[0])):
            if g.is_low(r, c):
                total += 1 + g.grid[r][c]

    return total

def part2() -> int:
    g = get_grid()
    sums = []

    for r in range(len(g.grid)):
        for c in range(len(g.grid[0])):
            res = g.basin(r,c)
            sums.append(res)

    sums.sort()
    i = len(sums)
    
    return sums[i-1] * sums[i-2] * sums[i-3]