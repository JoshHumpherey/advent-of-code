from typing import Dict
from lib.parse import parse_strings
from collections import defaultdict
from copy import deepcopy

def create_bricks() -> Dict[str, set]:
    data = parse_strings("2023/day22/input.txt")
    unsorted_bricks = []
    for d in data:
        ends = d.split("~")
        start, end = [[int(x) for x in e.split(",")] for e in ends]
        b = set()
        min_z = float('inf')
        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                for z in range(start[2], end[2]+1):
                    b.add((x,y,z))
                    min_z = min(min_z, z)
        unsorted_bricks.append([min_z, b])
    
    label = 0
    bricks = defaultdict(set)
    for _, b in sorted(unsorted_bricks):
        bricks[str(label)] = b
        label += 1

    return bricks

def settle_tower(bricks: Dict[str, set]) -> Dict[str, set]:
    settled_bricks = defaultdict(set)
    for label, cubes in bricks.items():
        curr = cubes
        while True:
            shifted, collision = set(), False
            for c in curr:
                x, y, z = c
                z -= 1
                shifted.add((x,y,z))
                if z <= 0:
                    collision = True
                    
            for settled in settled_bricks.values():
                for s in settled:
                    if s in shifted:
                        collision = True
                        
            if collision:
                settled_bricks[label] = curr
                break
            else:
                curr = shifted
            
    return settled_bricks    

def can_remove(target: str, bricks: Dict[str, set]) -> bool:
    test_bricks = deepcopy(bricks)
    del test_bricks[target]

    settled_test_bricks = settle_tower(bricks=test_bricks)
    return settled_test_bricks == test_bricks

def find_supports() -> int:
    bricks = create_bricks()
    settled_bricks = settle_tower(bricks=bricks)
    count = 0

    for label in settled_bricks.keys():
        if can_remove(target=label, bricks=settled_bricks):
            print(f"Safe to remove {label}")
            count += 1
    
    return count

print(find_supports())