from typing import List
from lib.parse import parse_strings
import z3

class Hailstone:

    def __init__(self, pos: List[int], vel: List[int]) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.vx = vel[0]
        self.vy = vel[1]
        self.vz = vel[2]
        
def count_collisions(hailstones: List[Hailstone], low_bound: int, high_bound: int) -> int:
    x, y, z = z3.Real('x'), z3.Real('y'), z3.Real('z')
    vx, vy, vz = z3.Real('vx'), z3.Real('vy'), z3.Real('vz')
    s = z3.Solver()
    for i in range(len(hailstones)):
        x_i, y_i, z_i = hailstones[i].x, hailstones[i].y, hailstones[i].z
        vx_i, vy_i, vz_i = hailstones[i].vx, hailstones[i].vy, hailstones[i].vz
        t_i = z3.Real(f"t_{i}")
        s.add(x_i + vx_i * t_i == x + vx * t_i)
        s.add(y_i + vy_i * t_i == y + vy * t_i)

    s.add(low_bound <= x, x <= high_bound)
    s.add(low_bound <= y, y <= high_bound)

    count = 0
    while s.check() == z3.sat:
        count += 1
        m = s.model()
        s.add(z3.Or(x != m[x], y != m[y]))

    return count

def create_hailstones() -> List[Hailstone]:
    data = parse_strings("2023/day24/input.txt")
    hailstones: List[Hailstone] = []
    for d in data:
        raw = d.split(" @ ")
        pos, vel = [[int(x) for x in y.split(", ")] for y in raw]
        print(pos, vel)
        hailstones.append(Hailstone(pos=pos, vel=vel))
    
    return hailstones

def find_collisions() -> int:
    hailstones = create_hailstones()
    return count_collisions(hailstones, 0, 40)

print(find_collisions())
