from typing import Dict, List, Tuple
from lib.parse import parse_string_groups
from collections import defaultdict

def parse_input():
    maps = parse_string_groups("2023/day5/input.txt")
    seeds = [int(x) for x in maps[0][0].split(" ")[1:]]
    ranges = []

    for i in range(1, len(maps)):
        print(maps[i])
        mapping = defaultdict(int)
        for j in range(1, len(maps[i])):
            row = [int(x) for x in maps[i][j].split(" ")]
            dest, source, to_add = row[0], row[1], row[2]
            for _ in range(to_add):
                mapping[source] = dest
                source += 1
                dest += 1
        ranges.append(mapping)

    return seeds, ranges
            
def get_smallest_location() -> int:
    seeds, ranges = parse_input()
    best = float('inf')

    for num in seeds:
        for range in ranges:
            if num in range:
                num = range[num]
        print(num)
        best = min(best, num)
    
    return best

print(get_smallest_location())

