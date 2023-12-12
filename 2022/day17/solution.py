from enum import Enum
import os
import time
from lib.parse import parse_strings

SIM_TIME = 0.1

class Shapes(Enum):
    HorizontalLine = [[0,2], [0,3], [0,4], [0,5], [0,6]]
    Cross = [[0,3], [1,3], [2,3], [1,2], [1,4]]
    Angle = [[0,4], [1,4], [2,4], [2,3], [2,2]]
    VeriticalLine = [[0,2], [1,2], [2,2], [3,2]]
    Square = [[0,2], [0,3], [1,2], [1,3]]

SHAPES = [Shapes.HorizontalLine, Shapes.Cross, Shapes.Angle, Shapes.VeriticalLine, Shapes.Square]
INIT_HEIGHT = {
    Shapes.HorizontalLine: 1,
    Shapes.Cross: 3,
    Shapes.Angle: 3,
    Shapes.VeriticalLine: 4,
    Shapes.Square: 2,
}

BEDROCK = "#"
ROCK = "@"
AIR = "."


class Tetris:

    def __init__(self, wind: str) -> None:
        self.grid = [[AIR for _ in range(8)] for _ in range(4)]
        self.wind = wind
        self.wind_idx = 0
        self.shape_idx = 0
        self.debug = False

    def print(self) -> None:
        if not self.debug:
            return
        
        os.system("clear")
        for row in self.grid:
            print("|" + "".join(row) + "|")
        print("----------")
        time.sleep(SIM_TIME)

    def initialize_block(self, block: Shapes) -> None:
        for r in range(0, 4):
            for c in range(len(self.grid[0])):
                if [r,c] in block.value:
                    self.grid[r][c] = ROCK

    def resolve_wind(self) -> None:
        dir = self.wind[self.wind_idx % len(self.wind)]
        left = True if dir == "<" else False
        self.wind_idx += 1
        
        to_shift = []
        shifted = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == ROCK:
                    to_shift.append([r,c])
            
        for i in range(len(to_shift)):
            if left:
                if to_shift[i][1] - 1 < 0 or self.grid[to_shift[i][0]][to_shift[i][1]-1] == BEDROCK:
                    return
                shifted.append([to_shift[i][0], to_shift[i][1]-1])
            else:
                if to_shift[i][1] + 1 >= len(self.grid[0]) or self.grid[to_shift[i][0]][to_shift[i][1]+1] == BEDROCK:
                    return
                shifted.append([to_shift[i][0], to_shift[i][1]+1])

        for row,col in to_shift:
            self.grid[row][col] = AIR
        for row, col in shifted:
            self.grid[row][col] = ROCK
        
        return

    def resolve_gravity(self) -> bool:
        hit_bottom = False
        to_shift = []
        shifted = []
        bedrock = set()

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == BEDROCK:
                    bedrock.add((r,c))
                elif self.grid[r][c] == ROCK:
                    to_shift.append([r,c])
        
        for i in range(len(to_shift)):
            if (to_shift[i][0]+1,to_shift[i][1]) in bedrock or to_shift[i][0]+1 >= len(self.grid):
                hit_bottom = True
                break
            else:
                shifted.append([to_shift[i][0]+1, to_shift[i][1]])
        
        if hit_bottom:
            for r,c in to_shift:
                self.grid[r][c] = BEDROCK
            return True
        
        for r,c in to_shift:
            self.grid[r][c] = AIR
        for r, c in shifted:
            self.grid[r][c] = ROCK

        return False
                
    def resize_grid(self) -> None:
        next_block = SHAPES[self.shape_idx % len(SHAPES)]
        block_padding = INIT_HEIGHT[next_block]
        existing_padding = 0
        found_rock = False
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] != AIR:
                    found_rock = True
                    break
            
            if found_rock:
                break
            existing_padding += 1
        
        required_padding = 3 + block_padding
        while required_padding > existing_padding:
            self.grid.insert(0, [AIR for _ in range(8)])
            required_padding -= 1
        
        while existing_padding > required_padding:
            self.grid.pop(0)
            existing_padding -= 1

        return

    def tower_height(self) -> int:
        existing_padding = 0
        found_rock = False
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] != AIR:
                    found_rock = True
                    break
            
            if found_rock:
                break
            existing_padding += 1

        return len(self.grid) - existing_padding

    def drop_block(self):
        self.initialize_block(block=SHAPES[self.shape_idx % len(SHAPES)])
        self.shape_idx += 1

        self.print()
        while True:
            self.resolve_wind()
            self.print()
            if self.resolve_gravity():
                break
            self.print()

        self.print()
        self.resize_grid()

def part_1() -> None:
    wind = parse_strings("2022/day17/input.txt")[0]
    tetris = Tetris(wind)
    tetris.debug = True
    for i in range(10):
        if i % 10 == 0:
            print(f"Simulating block {i}")
        tetris.drop_block()
    
    return tetris.tower_height()
    
print(part_1())
