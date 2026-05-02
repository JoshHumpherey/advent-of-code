from dataclasses import dataclass
from typing import Iterator, List

@dataclass
class Pair:
    x: int
    y: int

@dataclass
class Line:
    p1: Pair
    p2: Pair

@dataclass
class Grid:
    size = 1_000
    def __post_init__(self):
        self.grid = []
        for _ in range(self.size):
            grid_row = []
            for _ in range(self.size):
                grid_row.append(0)
            self.grid.append(grid_row)

    def print(self) -> None:
        print()
        for r in range(len(self.grid)):
            prett_row = ""
            for c in range(len(self.grid[0])):
                prett_row += str(self.grid[r][c])
            print(prett_row)
        print()
    
    def count(self, threshold: int) -> int:
        total = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] >= threshold:
                    total += 1
        
        return total


def points_on_line(line: Line) -> Iterator[Pair]:
    dx = line.p2.x - line.p1.x
    dy = line.p2.y - line.p1.y

    if dx != 0 and dy != 0 and abs(dx) != abs(dy):
        raise ValueError(f"unsupported line: {line}")

    step_x = 0 if dx == 0 else dx // abs(dx)
    step_y = 0 if dy == 0 else dy // abs(dy)
    steps = max(abs(dx), abs(dy))

    for step in range(steps + 1):
        yield Pair(
            x=line.p1.x + step * step_x,
            y=line.p1.y + step * step_y,
        )


def get_input() -> List[Line]:
    with open('input.txt', 'r') as file:
        lines = []
        for line in file:
            l = line.strip()
            raw1, raw2 = l.split(' -> ')
            data1, data2 = raw1.split(','), raw2.split(',')
            p1, p2 = Pair(int(data1[0]), int(data1[1])), Pair(int(data2[0]), int(data2[1]))
            lines.append(Line(p1, p2))

        return lines

def count_overlaps(lines: List[Line], count_diagonal: bool, threshold: int) -> int:
    grid = Grid()
    for l in lines:
        points = []
        if (l.p1.x == l.p2.x or l.p1.y == l.p2.y) or count_diagonal:
            points = points_on_line(line=l)
        elif count_diagonal:
            points = points_on_line(line=l)

        for p in points:
            grid.grid[p.y][p.x] += 1
    
    return grid.count(threshold=threshold)


puzzle_input = get_input()

p1 = count_overlaps(lines=puzzle_input, count_diagonal=False, threshold=2)
print(p1)

p2 = count_overlaps(lines=puzzle_input, count_diagonal=True, threshold=2)
print(p2)