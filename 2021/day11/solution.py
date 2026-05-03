from typing import List

class Octopus:

    def __init__(self, val: int, flashed: bool = False) -> None:
        self.val = val
        self.flashed = flashed

class Grid:

    def __init__(self, nums: List[List[int]]):
        self.octo: List[List[Octopus]] = []
        self.threshold = 9

        for r in range(len(nums)):
            row = []
            for c in range(len(nums[0])):
                row.append(Octopus(val=nums[r][c]))
            self.octo.append(row)

    def flash(self, r: int, c: int) -> None:
        if r < 0 or c < 0 or r >= len(self.octo) or c >= len(self.octo[0]):
            return
        elif self.octo[r][c].flashed:
            return
        else:
            self.octo[r][c].val += 1
            if self.octo[r][c].val > self.threshold:
                self.octo[r][c].val = 0
                self.octo[r][c].flashed = True
                adj = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1],  [1, 0],  [1, 1]]
                for r_offset, c_offset in adj:
                    self.flash(r+r_offset, c+c_offset)
    
    def reset_flashes(self) -> int:
        flashed = 0
        for r in range(len(self.octo)):
            for c in range(len(self.octo[0])):
                if self.octo[r][c].flashed:
                    flashed += 1
                    self.octo[r][c].flashed = False
        return flashed
    
    def increment(self) -> List[List[int]]:
        to_flash = []
        for r in range(len(self.octo)):
            for c in range(len(self.octo[0])):
                self.octo[r][c].val += 1
                if self.octo[r][c].val > self.threshold:
                    to_flash.append([r,c])
        return to_flash


    def cycle(self) -> int:
        to_flash = self.increment()
        for r,c in to_flash:
            self.flash(r,c)
        return self.reset_flashes()



def get_grid() -> Grid:
    with open('input.txt') as f:
        lines = f.readlines()
        data = []
        for l in lines:
            row = []
            numstrs = l.strip()
            for s in numstrs:
                row.append(int(s.strip()))
            data.append(row)
        return Grid(nums=data)

def get_flash_count(g: Grid, cycles: int):
    total = 0
    for _ in range(cycles):
        total += g.cycle()
    return total

def get_simultaneous_count(g: Grid) -> int:
    cycles = 0
    total_cells = len(g.octo) * len(g.octo[0])
    while True:
        cycles += 1
        flashes = g.cycle()
        if flashes == total_cells:
            return cycles


p1 = get_flash_count(get_grid(), 100)
print(p1)

p2 = get_simultaneous_count(get_grid())
print(p2)