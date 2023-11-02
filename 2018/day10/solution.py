from lib.parse import parse_strings
from lib.initialize import create_grid
from lib.pretty_print import print_grid
from typing import Tuple, List
import time
import os
import re

SIMULATION_DURATION = 0.5
SIMULATION_LENGTH = 100_000
PATTERN = r'position=<\s*([-+]?\d+),\s*([-+]?\d+)> velocity=<\s*([-+]?\d+),\s*([-+]?\d+)>'
BOUND = 100

class Point:

    def __init__(self, raw_pos: List[int], raw_vel: List[int]) -> None:
        self.pos = raw_pos[::-1]
        self.vel = raw_vel[::-1]

    def print(self) -> None:
        print(f"Position: {self.pos}, Velocity: {self.vel}")

def create_points() -> Tuple[List[Point], int, int]:
    data = parse_strings("2018/day10/input.txt")
    points = []
    row_max, col_max = 0, 0
    row_min, col_min = float('inf'), float('inf')
    
    for d in data:
        matches = re.findall(PATTERN, d)
        x_pos, y_pos, x_vel, y_vel = map(int, matches[0])
        p = Point(raw_pos=[int(x_pos), int(y_pos), ], raw_vel=[int(x_vel), int(y_vel)])
        points.append(p)
        row_max = max(row_max, p.pos[0])
        col_max = max(col_max, p.pos[1])
        row_min = min(row_min, p.pos[0])
        col_min = min(col_min, p.pos[1])
    
    row_offset = 0 if row_min >= 0 else abs(row_min)
    col_offset = 0 if col_min >= 0 else abs(col_min)

    for p in points:
        p.pos[0] += row_offset
        p.pos[1] += col_offset
    
    return points, row_max+row_offset, col_max+col_offset

def advance_simulation(points: List[Point], row_max: int, col_max: int) -> List[Point]:
    for p in points:
        p.pos[0] = (p.pos[0] + p.vel[0]) % (row_max + 1)
        p.pos[1] = (p.pos[1] + p.vel[1]) % (col_max + 1)
    return points

def get_bounds(points: List[Point]) -> Tuple[List[int], List[int]]:
    r_min, r_max = float('inf'), 0
    c_min, c_max = float('inf'), 0
    for p in points:
        r_min = min(r_min, p.pos[0])
        r_max = max(r_max, p.pos[0])
        c_min = min(c_min, p.pos[1])
        c_max = max(c_max, p.pos[1])
    
    return [r_min, r_max], [c_min, c_max]


def simulate_lights() -> None:
    points, row_max, col_max = create_points()
    for i in range(SIMULATION_LENGTH):
        r_bounds, c_bounds = get_bounds(points)
        r_diff = abs(r_bounds[0] - r_bounds[1])
        c_diff = abs(c_bounds[0] - c_bounds[1]) 
       
        if r_diff <= BOUND and  c_diff <= BOUND:
            print(f"TIME: {i}")
            for r in range(r_bounds[0], r_bounds[1]+1):
                pretty = ""
                for c in range(c_bounds[0], c_bounds[1]+1):
                    found = False
                    for p in points:
                        if p.pos == [r, c]:
                            pretty += "#"
                            found = True
                            break
                    if not found:
                        pretty += "."
                print(pretty)

            time.sleep(SIMULATION_DURATION)
        points = advance_simulation(points, row_max, col_max)
    
simulate_lights()
