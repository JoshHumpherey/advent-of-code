from enum import Enum
import sys
from typing import List
from lib.parse import parse_strings

class Direction(Enum):
    U = [-1, 0],
    D = [1, 0],
    L = [0, -1],
    R = [0, 1],

class Instruction:

    def __init__(self, raw_ins: str) -> None:
        data = raw_ins.split(" ")
        self.dir = Direction[data[0]]
        self.len = int(data[1])
        self.hex = data[2][1:len(data[2])-1]
    
    def print(self):
        print(f"Dir: {self.dir.name}, Len: {self.len}, Hex: {self.hex}")

class Cell:

    def __init__(self, color: str = "", depth: int = 0):
        self.color = color
        self.depth = depth

class Grid:

    def __init__(self) -> None:
        self.grid: List[List[Cell]] = [[Cell()]]
        self.r = 0
        self.c = 0
    
    def add_col(self):
        for r in range(len(self.grid)):
            self.grid[r].extend([Cell()])
    
    def add_row(self):
        to_insert = [Cell() for _ in range(len(self.grid[0]))]
        self.grid.append(to_insert)
    
    def print(self):
        for r in range(len(self.grid)):
            row = ""
            for c in range(len(self.grid[0])):
                if self.grid[r][c].depth == 0:
                    row += "."
                else:
                    row += str(self.grid[r][c].depth)
            print(row)
        print()

    def execute(self, ins: Instruction):
        for _ in range(ins.len):
            self.r, self.c = self.r + ins.dir.value[0][0], self.c + ins.dir.value[0][1]
            while self.r >= len(self.grid):
                self.add_row()
            while self.c >= len(self.grid[0]):
                self.add_col()

            self.grid[self.r][self.c].depth += 1
            self.grid[self.r][self.c].color = ins.hex

    def flood(self, r: int, c: int, target: int, val: int) -> None:
        if r < 0 or c < 0 or r >= len(self.grid) or c >= len(self.grid[0]) or self.grid[r][c].depth != target:
            return
        self.grid[r][c].depth = val
        self.flood(r+1, c, target, val)
        self.flood(r-1, c, target, val)
        self.flood(r, c+1, target, val)
        self.flood(r, c-1, target, val)

    def fill_enclosed(self) -> int:
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if (r == 0 or c == 0 or r == len(self.grid)-1 or c == len(self.grid[0])-1) and self.grid[r][c].depth == 0:
                    self.flood(r, c, 0, -1)

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].depth == 0:
                    self.grid[r][c].depth = 1
                elif self.grid[r][c].depth == -1:
                    self.grid[r][c].depth = 0

        area = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].depth >= 1:
                    area += 1

        return area

def get_instructions() -> List[Instruction]:
    data = parse_strings("2023/day18/input.txt")
    ins = []
    for d in data:
        ins.append(Instruction(raw_ins=d))
    return ins

def get_cubic_depth() -> int:
    ins = get_instructions()
    grid = Grid()

    for i in ins:
        if i.dir == Direction.L:
            for _ in range(i.len):
                grid.add_col()
                grid.c += 1
        elif i.dir == Direction.U:
            for _ in range(i.len):
                grid.add_row()
                grid.r += 1

    for i in ins:
        grid.execute(ins=i)
    grid.add_col()
    grid.add_row()

    res = grid.fill_enclosed()
    return res

sys.setrecursionlimit(1_000_000_000)
print(get_cubic_depth())
