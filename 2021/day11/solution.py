DAYS = 100

class Grid:

    class Octo:

        def __init__(self, val):
            self.val = val
            self.flashed = False

    def __init__(self, numbers):
        self.grid = [ [0]*len(numbers[0]) for _ in range(len(numbers)) ]
        for r in range(0, len(numbers)):
            for c in range(0, len(numbers[0])):
                self.grid[r][c] = self.Octo(val=numbers[r][c])
        self.threshold = 9
        self.baseline = 0

    def get_surrounding_cells(self, r, c):
        return  [[r+1,c],[r-1,c],[r,c+1],[r,c-1],[r+1, c+1],[r-1, c-1],[r+1, c-1],[r-1, c+1],]

    def flash(self, r, c) -> int:
        flashes = 1
        self.grid[r][c].flashed = True
        self.grid[r][c].val = self.baseline
        
        queue = self.get_surrounding_cells(r,c)
        while queue:
            next_queue = []
            for row, col in queue:
                if row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[0]) and not self.grid[row][col].flashed:
                    self.grid[row][col].val += 1
                    if self.grid[row][col].val > self.threshold:
                        flashes += 1
                        self.grid[row][col].val = self.baseline
                        self.grid[row][col].flashed = True
                        nearby = self.get_surrounding_cells(row, col)
                        for n in nearby:
                            next_queue.append(n)
            queue = next_queue
        return flashes
            
    def simulate_cycle(self) -> bool:
        flashes = 0
        
        # Account for general energy increase
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                self.grid[r][c].val += 1

        # Account for flashes triggering other flashes
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].val > self.threshold and not self.grid[r][c].flashed:
                    flashes += self.flash(r,c)
        
        # Reset grid flash indicators and check if sync'd
        sync = True
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].flashed: 
                    self.grid[r][c].flashed = False
                else:
                    sync = False
        return sync

    def print(self) -> None:
        for row in self.grid:
            data = []
            for oct in row:
                data.append(oct.val)
            print(data)


def get_grid() -> Grid:
    with open('day11/input.txt') as f:
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
    flashes = 0
    
    for day in range(1, 1000):
        print(f"Simulating day {day}")
        sync = g.simulate_cycle()
        g.print()
        if sync:
            return day

    return flashes