from enum import Enum
import os
import time
from typing import List, Tuple
import uuid
from lib.parse import parse_string_grid

class Type(Enum):
    GOBLIN = "G"
    ELF = "E"

class Unit:

    def __init__(self, r: int, c: int, raw_type: str) -> None:
        self.id = str(uuid.uuid4())
        self.type = Type.GOBLIN if raw_type == Type.GOBLIN.value else Type.ELF
        self.r = r
        self.c = c
        self.hp = 200
        self.ap = 3

    def is_hostile(self, target_type: Type) -> bool:
        return self.type != target_type

    def move(self, grid: List[List[str]], units: List['Unit']) -> None:
        best_path = []
        for u in units:
            if u.id != self.id and self.is_hostile(u.type):
                temp_path = generate_path_to_unit(grid=grid, base=self, target=u)
                if len(temp_path) > 0 and (len(temp_path) < len(best_path) or best_path == []):
                    best_path = temp_path
        
        if len(best_path) <= 1:
            return

        self.r, self.c = best_path[0][0], best_path[0][1]
    
def generate_path_to_unit(grid: List[List[str]], base: Unit, target: Unit):
    queue = [(base.r, base.c, [])]
    seen = set()
    steps = 0

    while queue:
        next_queue = []
        steps += 1
        for r, c, path in queue:
            if (r, c) in seen:
                continue
            elif (r, c) == (target.r, target.c):
                return path
            
            seen.add((r, c))
            if grid[r][c] != "." and (r, c) != (base.r, base.c):
                continue
            
            next_steps = [(-1,0), (0,-1), (0,1), (1,0)]
            for x,y in next_steps:
                next_r, next_c = r+x, c+y
                if next_r >= 0 and next_r < len(grid) and next_c >= 0 and next_c < len(grid[0]) and (next_r, next_c) not in seen:
                    next_queue.append([next_r, next_c, path + [(next_r, next_c)]])
        queue = next_queue
    
    return []

def print_grid_with_overlay(grid: List[List[str]], units: List[Unit]) -> None:
    os.system("clear")
    for r in range(len(grid)):
        pretty = ""
        for c in range(len(grid[0])):
            detected = False
            for u in units:
                if [r,c] == [u.r,u.c]:
                    detected = True
                    pretty += u.type.value
                    break
            if not detected:
                pretty += grid[r][c]
        print(pretty)
    time.sleep(1)
    

def example() -> None:
    grid = parse_string_grid("2018/day15/input.txt")
    units: List[Unit] = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in [Type.GOBLIN.value, Type.ELF.value]:
                units.append(Unit(r=r, c=c, raw_type=grid[r][c]))
                grid[r][c] = "."

    print_grid_with_overlay(grid, units)
    for _ in range(3):
        units = sorted(units, key=lambda unit: (unit.r, unit.c))
        for u in units:
            u.move(grid, units)
            print_grid_with_overlay(grid, units)
    
example()
