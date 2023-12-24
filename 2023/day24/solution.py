from typing import List
from lib.parse import parse_strings
import numpy as np
import z3

class Hailstone:

    def __init__(self, pos: List[int], vel: List[int]) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.vx = vel[0]
        self.vy = vel[1]
        self.vz = vel[2]
    
    def info(self) -> str:
        return f"Pos: {self.x, self.y, self.z}, Vel: {self.vx, self.vy, self.vz}"

def create_hailstones() -> List[Hailstone]:
    data = parse_strings("2023/day24/input.txt")
    hailstones: List[Hailstone] = []
    for d in data:
        raw = d.split(" @ ")
        pos, vel = [[int(x) for x in y.split(", ")] for y in raw]
        hailstones.append(Hailstone(pos=pos, vel=vel))
    
    return hailstones

def collisions_within_bounds(hailstones: List[Hailstone], low_bound: int, high_bound: int):
    collisions = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            h1, h2 = hailstones[i], hailstones[j]
            if h2.vy == 0 or h1.vy == 0 or (h1.vx / h1.vy - h2.vx / h2.vy) == 0:
                continue
            y = (h2.x - (h2.vx / h2.vy * h2.y) + (h1.vx / h1.vy * h1.y) - h1.x) / (h1.vx / h1.vy - h2.vx / h2.vy)
            x = ((y - h1.y) / h1.vy) * h1.vx + h1.x
            if (low_bound <= x <= high_bound and low_bound <= y <= high_bound):
                if (np.sign(x - h1.x) == np.sign(h1.vx) and np.sign(y - h1.y) == np.sign(h1.vy) and np.sign(x - h2.x) == np.sign(h2.vx) and np.sign(y - h2.y) == np.sign(h2.vy)):
                    collisions += 1
    return collisions

def collide_with_all(hailstones: List[Hailstone]) -> int:
    s = z3.Solver()
    x, y, z, vx, vy, vz = [z3.Int(var) for var in ["x", "y", "z", "vx", "vy", "vz"]]
    for i in range(0, 3):
        h = hailstones[i]
        t = z3.Int(f"t{i}")
        s.add(t >= 0)
        s.add(x + vx * t == h.x + h.vx * t)
        s.add(y + vy * t == h.y + h.vy * t)
        s.add(z + vz * t == h.z + h.vz * t)
    if s.check() == z3.sat:
        m = s.model()
        print(m)
        return int(m[x].as_long() + m[y].as_long() + m[z].as_long())
    else:
        return -1

def find_collisions() -> int:
    hailstones = create_hailstones()
    return collisions_within_bounds(hailstones, 200000000000000, 400000000000000)

def find_all_collisions() -> int:
    hailstones = create_hailstones()
    return collide_with_all(hailstones)

print(find_collisions())
print(find_all_collisions())