from collections import defaultdict
import heapq

class Grid:

    def __init__(self, numbers):
        self.grid = [ [0]*len(numbers[0]) for _ in range(len(numbers)) ]      
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                self.grid[r][c] = numbers[r][c]

        self.costs = defaultdict(int)
        
    
    def optimal_path(self) -> int:
        min_heap, visited = [(0, 0, 0)], set()
        heapq.heapify(min_heap)
        
        while min_heap:
            local_cost, r, c = heapq.heappop(min_heap)
            if (r,c) in visited:
                continue
            
            visited.add((r,c))
            self.costs[(r,c)] = local_cost
            if r == len(self.grid)-1 and c == len(self.grid[0]):
                break
            
            adj = [(1,0), (0,1), (-1,0), (0,-1)]
            for x,y in adj:
                rr, cc = r+x, c+y
                if not (0 <= rr < len(self.grid) and 0 <= cc < len(self.grid[0])):
                    continue
                
                
                heapq.heappush(min_heap, (local_cost+self.grid[rr][cc], rr, cc))

        return self.costs[len(self.grid)-1, len(self.grid[0])-1]
                
                            

            
        
        
                   
def create_grid() -> Grid:
    with open('day15/input.txt') as f:
        lines = f.readlines()
        numbers = []
        for l in lines:
            l = l.strip()
            
            row = []
            for char in l:

                row.append(int(char))
            numbers.append(row)
        return Grid(numbers=numbers)

def part1() -> int:
    grid = create_grid()
    return grid.optimal_path()

def part2() -> int:
    with open("day15/input.txt") as fin:
        raw_data = fin.read().strip()
        map = [[int(i) for i in line] for line in raw_data.split("\n")]
        
        
        N = len(map)
        M = len(map[0])
        
        rows = N * 5
        cols = M * 5
        
        
        def get(r, c):
            x = (map[r % N][c % M] +
                 (r // N) + (c // M))
            return (x - 1) % 9 + 1
        
        
        cost = defaultdict(int)
        
        pq = [(0, 0, 0)]
        heapq.heapify(pq)
        visited = set()
        
        while len(pq) > 0:
            c, row, col = heapq.heappop(pq)
        
            if (row, col) in visited:
                continue
            visited.add((row, col))
        
            cost[(row, col)] = c
        
            if row == rows - 1 and col == cols - 1:
                break
        
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                rr = row + dr
                cc = col + dc
                if not (0 <= rr < rows and 0 <= cc < cols):
                    continue
        
                heapq.heappush(pq, (c + get(rr, cc), rr, cc))
        
        
        print(cost[(rows - 1, cols - 1)])
