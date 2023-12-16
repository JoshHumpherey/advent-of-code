from enum import Enum
import os
import time
from typing import List
from lib.parse import parse_string_grid

DELAY = 0.5

EMPTY = "."
VERT = "|"
HORIZ = "-"
FORWARD = "/"
BACK = "\\"

class Direction(Enum):
    NORTH = [-1,0]
    SOUTH = [1, 0]
    WEST = [0, -1]
    EAST = [0, 1]

class Beam:

    def __init__(self, r: int, c: int, dir: Direction):
        self.r = r
        self.c = c
        self.dir = dir
    
    def advance(self) -> None:
        self.r += self.dir.value[0]
        self.c += self.dir.value[1]
        return
    
class Grid:

    def __init__(self, data: List[List[str]]) -> None:
        self.grid = data
        self.seen = [[set() for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.energized = set()

    def print(self, beams: List[Beam]):
        os.system("clear")
        for r in range(len(self.grid)):
            row = ""
            for c in range(len(self.grid[0])):
                added_beam = False
                for b in beams:
                    if not added_beam and b.r == r and b.c == c:
                        added_beam = True
                if added_beam:
                    row += "@"
                else:
                    row += self.grid[r][c]
            print(row)
        print()
        time.sleep(DELAY)

    def get_new_beams(self, s: str, b: Beam) -> List[Beam]:
        next_beams = []
        if s == EMPTY:
            next_beams.append(b)
        elif s == VERT:
            if b.dir in {Direction.WEST, Direction.EAST}:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.NORTH))
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.SOUTH))
            else:
                next_beams.append(Beam(r=b.r, c=b.c, dir=b.dir))
        elif s == HORIZ:
            if b.dir in {Direction.NORTH, Direction.SOUTH}:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.WEST))
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.EAST))
            else:
                next_beams.append(Beam(r=b.r,c=b.c,dir=b.dir))
        elif s == FORWARD:
            if b.dir == Direction.NORTH:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.EAST))
            elif b.dir == Direction.EAST:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.NORTH))
            elif b.dir == Direction.SOUTH:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.WEST))
            elif b.dir == Direction.WEST:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.SOUTH))
            else:
                raise Exception(f"Unknown Beam Direction: {b.dir.name}")
        elif s == BACK:
            if b.dir == Direction.NORTH:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.WEST))
            elif b.dir == Direction.EAST:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.SOUTH))
            elif b.dir == Direction.SOUTH:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.EAST))
            elif b.dir == Direction.WEST:
                next_beams.append(Beam(r=b.r, c=b.c, dir=Direction.NORTH))
            else:
                raise Exception(f"Unknown Beam Direction: {b.dir.name}")    
        else:
            raise Exception(f"Unknown Tile: {s}")
        return next_beams
    
    def shoot_beams(self, start: Beam):
        beams = [start]
        # self.print(beams)
        while beams:
            next_beams = []
            for b in beams:
                self.energized.add((b.r, b.c))
                b.advance()
                if b.r < 0 or b.c < 0 or b.r >= len(self.grid) or b.c >= len(self.grid[0]):
                    continue
                elif b.dir in self.seen[b.r][b.c]:
                    continue
                
                s = self.grid[b.r][b.c]
                self.seen[b.r][b.c].add(b.dir)
                next_beams.extend(self.get_new_beams(s, b))
                
            beams = next_beams
            # self.print(beams)

def get_energized_area() -> int:
    data = parse_string_grid("2023/day16/input.txt")
    grid = Grid(data)
    grid.shoot_beams(start=Beam(r=0,c=-1,dir=Direction.EAST))
    return len(grid.energized) - 1

def get_best_starting_config() -> int:
    data = parse_string_grid("2023/day16/input.txt")
    best = 0
    for r in range(len(data)):
        for c in range(len(data[0])):
            grid = Grid(data)
            if r == 0:
                grid.shoot_beams(start=Beam(r-1, c, Direction.SOUTH))
            elif r == len(data)-1:
                grid.shoot_beams(start=Beam(r+1, c, Direction.NORTH))
            elif c == 0:
                grid.shoot_beams(start=Beam(r, c-1, Direction.EAST))
            elif c == len(data[0])-1:
                grid.shoot_beams(start=Beam(r, c-1, Direction.WEST)) 
            best = max(best, len(grid.energized)-1)            
    return best

print(get_energized_area())
print(get_best_starting_config())
