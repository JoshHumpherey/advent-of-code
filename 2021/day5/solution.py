from bresenham import bresenham

GRID_SIZE = 1000

class Coordinate:
    def __init__(self, c, r):
        self.c = c
        self.r = r

    def to_pair(self):
        return [self.c, self.r]
            
class Map:
        
    def __init__(self):
        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.threshold = 1
        
    def add_line(self, p1: Coordinate, p2: Coordinate) -> None:
        if p1.c == p2.c: # straight vertical line
            for r in range(min(p1.r, p2.r), max(p1.r, p2.r)+1):
                self.grid[r][p1.c] += 1
        elif p1.r == p2.r: # straight horizontal line 0,9 -> 5,9
            for c in range(min(p1.c, p2.c), max(p1.c, p2.c)+1):
                self.grid[p1.r][c] += 1
        else: # diagonal
            self.plot_diagonal(p1, p2)
            
    def plot_diagonal(self, p1: Coordinate, p2: Coordinate):
        """ Plot using Breshnam's Algorithm """
        points = list(bresenham(p1.c, p1.r, p2.c, p2.r))
        for r, c in points:
            self.grid[c][r] += 1
        return
            
    def intersections(self) -> int:
        count = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] > self.threshold:
                    count += 1
        return count

    def print(self) -> None:
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 0:
                    self.grid[r][c] = '.'
                else:
                    self.grid[r][c] = str(self.grid[r][c])

        for row in self.grid:
            print(row)
                



def create_pairs():
    pairs = []
    with open('day5/input.txt') as f:
        lines = f.readlines()
        for l in lines:
            p1, p2 = l.split('->')
            p1 = p1.strip()
            p2 = p2.strip()

            x1, y1 = p1.split(',')
            x2, y2 = p2.split(',')
            x1, y1 = int(x1), int(y1)
            x2, y2 = int(x2), int(y2)
            pairs.append([Coordinate(x1, y1), Coordinate(x2, y2)])
    return pairs

def part1() -> int:
    pairs = create_pairs()
    m = Map()

    for p1, p2 in pairs:
        m.add_line(p1, p2)

    return m.intersections()
    

def part2() -> int:
    pairs = create_pairs()
    m = Map()

    for p1, p2 in pairs:
        m.add_line(p1, p2)

    return m.intersections()