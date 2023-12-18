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

def get_instructions() -> List[Instruction]:
    data = parse_strings("2023/day18/input.txt")
    ins = []
    for d in data:
        ins.append(Instruction(raw_ins=d))
    return ins

def shoelace(points):
    if points[0] != points[-1]:
        points.append(points[0])

    area = 0
    perim = 0
    for i in range(1, len(points)):
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        area += (x1 * y2 - x2 * y1)
        perim += abs(x2 - x1) + abs(y2 - y1)

    area = int(abs(area))
    return ((area + perim) // 2) + 1

def get_cubic_depth() -> int:
    ins = get_instructions()
    r, c = 0, 0
    coords = [[0,0]]
    for i in ins:
        if i.dir == Direction.U:
            r -= i.len
        elif i.dir == Direction.D:
            r += i.len
        elif i.dir == Direction.L:
            c -= i.len
        else:
            c += i.len
        coords.append([r,c])

    return shoelace(coords)

print(get_cubic_depth())
